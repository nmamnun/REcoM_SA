#include "SEAICE_OPTIONS.h"
#ifdef ALLOW_ECCO
# include "ECCO_OPTIONS.h"
#endif
#ifdef ALLOW_CTRL
# include "CTRL_OPTIONS.h"
#endif
#ifdef ALLOW_COST
# include "COST_OPTIONS.h"
#endif

c read the area dat file and compare against the averaged salinity file

      subroutine seaice_cost_sss(
     &     nnzbar, localbarfile, localbar, xx_localbar_mean_dummy,
     &             areabarfile,   areabar, xx_areabar_mean_dummy,
     &     nnzobs, localobsfile, localobs, mult_local,
     &     nrecloc, localstartdate, localperiod,
     &     localmask, localweight,
     &     spminloc, spmaxloc, spzeroloc,
     &     objf_local, num_local,
     &     myIter, myTime, myThid )

      implicit none

c ian fenty
c     == global variables ==

#include "EEPARAMS.h"
#include "SIZE.h"
#include "PARAMS.h"
#ifdef ALLOW_CAL
# include "cal.h"
#endif
#ifdef ALLOW_COST
# ifdef ALLOW_CTRL
#  include "optim.h"
# endif
# ifdef ALLOW_ECCO
#  include "ECCO_SIZE.h"
#  include "ECCO.h"
# endif
# ifdef ALLOW_SEAICE
#  include "SEAICE_COST.h"
#  include "SEAICE_SIZE.h"
#  include "SEAICE_PARAMS.h"
# endif
#endif

c     == routine arguments ==

      integer nnzbar
      integer nnzobs
      integer nrecloc
      integer myIter
      integer myThid
      integer localstartdate(4)

      _RL localbar   (1-OLx:sNx+OLx,1-OLy:sNy+OLy,nnzbar,nSx,nSy)
      _RL areabar   (1-OLx:sNx+OLx,1-OLy:sNy+OLy,nnzbar,nSx,nSy)

      _RL localobs   (1-OLx:sNx+OLx,1-OLy:sNy+OLy,nnzobs,nSx,nSy)
      _RL localweight(1-OLx:sNx+OLx,1-OLy:sNy+OLy,nSx,nSy)
      _RS localmask  (1-OLx:sNx+OLx,1-OLy:sNy+OLy,nr,nSx,nSy)
      _RL xx_localbar_mean_dummy
      _RL xx_areabar_mean_dummy
      _RL mult_local
      _RL myTime
      _RL localperiod
      _RL spminloc
      _RL spmaxloc
      _RL spzeroloc
      _RL objf_local(nSx,nSy)
      _RL num_local(nSx,nSy)

      character*(MAX_LEN_FNAM) areabarfile
      character*(MAX_LEN_FNAM) localbarfile
      character*(MAX_LEN_FNAM) localobsfile

#if (defined (ALLOW_ECCO) && defined (ALLOW_COST))
#ifdef ALLOW_SEAICE_COST_SMR_AREA

c     == local variables ==

      integer bi,bj
      integer i,j,k
      integer itlo,ithi
      integer jtlo,jthi
      integer jmin,jmax
      integer imin,imax
      integer irec
      integer  il
      integer localrec
      integer obsrec

      logical doglobalread
      logical ladinit

      _RL spval
      parameter (spval = -9999. )
      _RL localwww
      _RL localcost
      _RL junk

      _RL cmask (1-OLx:sNx+OLx,1-OLy:sNy+OLy,nnzobs)

      character*(128) fname1, fname2,fname3

cnew(
      _RL daytime
      _RL diffsecs
      integer dayiter
      integer daydate(4)
      integer difftime(4)
      integer middate(4)
      integer yday, ymod
      integer md, dd, sd, ld, wd
      logical exst
cnew)

c     == external functions ==

      integer  ilnblnk
      external ilnblnk

c     == end of interface ==

      jtlo = myByLo(myThid)
      jthi = myByHi(myThid)
      itlo = myBxLo(myThid)
      ithi = myBxHi(myThid)
      jmin = 1
      jmax = sNy
      imin = 1
      imax = sNx

c--   Initialise local variables.

      localwww = 0. _d 0

      do bj = jtlo,jthi
        do bi = itlo,ithi
          objf_local(bi,bj) = 0. _d 0
          num_local(bi,bj) = 0. _d 0
        enddo
      enddo

c--   First, read tiled data.
      doglobalread = .false.
      ladinit      = .false.

      write(fname1(1:128),'(80a)') ' '
csss
      write(fname3(1:128),'(80a)') ' '

      il=ilnblnk( localbarfile )
      write(fname1(1:128),'(2a,i10.10)')
     &     localbarfile(1:il),'.',optimcycle

csss
      il=ilnblnk( areabarfile )
      write(fname3(1:128),'(2a,i10.10)')
     &     areabarfile(1:il),'.',optimcycle

      if ( .NOT. ( localobsfile.EQ.' ' ) ) then

c--   Loop over records for the second time.
      do irec = 1, nrecloc

        if ( nnzbar .EQ. 1 ) then
           call active_read_xy( fname1, localbar, irec, doglobalread,
     &                      ladinit, optimcycle, myThid,
     &                      xx_localbar_mean_dummy )
        else
           call active_read_xyz( fname1, localbar, irec, doglobalread,
     &                       ladinit, optimcycle, myThid,
     &                       xx_localbar_mean_dummy )
        endif

csss
        if ( nnzbar .EQ. 1 ) then
           call active_read_xy( fname3, areabar, irec, doglobalread,
     &                      ladinit, optimcycle, myThid,
     &                      xx_areabar_mean_dummy )
        else
           call active_read_xyz( fname3, areabar, irec, doglobalread,
     &                       ladinit, optimcycle, myThid,
     &                       xx_areabar_mean_dummy )
        endif

cnew(
      obsrec = irec

      daytime = FLOAT(secondsperday*(irec-1)) + modelstart
      dayiter = hoursperday*(irec-1)+modeliter0

      call cal_getdate( dayiter, daytime, daydate, myThid )
      call cal_convdate( daydate,yday,md,dd,sd,ld,wd,myThid )
      ymod = smrareastartdate(1)/10000

#ifdef SEAICE_DEBUG
      print *,'cost_seaice_sss'
      print *,'daydate        ', daydate
      print *,'areaobsfile:  ', localobsfile
      print *,'nrecloc        ', nrecloc
      print *,'obsrec,daytime ', obsrec,daytime
      print *,'dayiter        ', dayiter
      print *,'yday :         ', yday
      print *,'md,dd,sd       ', md,dd,sd
      print *,'ld,wd          ', ld,wd
      print *,'loclstrtdte(1) ', localstartdate(1)
      print *,'ymod, yday     ', ymod,yday
      print *,'smrarstrtdt(1) ', smrareastartdate(1)
      print *,'smrarstartdate ', smrareastartdate
#endif /* SEAICE_DEBUG */

      if ( ymod .EQ. yday ) then
         middate(1) = smrareastartdate(1)
      else
         middate(1) = yday*10000+100+1
      endif
      middate(2) = 0
      middate(3) = modelstartdate(3)
      middate(4) = modelstartdate(4)

      call cal_TimePassed( middate, daydate, difftime, myThid )
      call cal_ToSeconds( difftime, diffsecs, myThid )

      localrec = int(diffsecs/localperiod) + 1

#ifdef SEAICE_DEBUG
      print *,'middate(1,2)     ',middate(1),middate(2)
      print *,'middate(3,4)     ', middate(3),middate(4)
      print *,'difftime,diffsecs',difftime,diffsecs
      print *,'localrec         ',localrec
#endif

      il=ilnblnk(localobsfile)
      write(fname2(1:128),'(2a,i4)')
     &      localobsfile(1:il), '_', yday
      inquire( file=fname2, exist=exst )

#ifdef SEAICE_DEBUG
      print *,'fname2',fname2
#endif
        if (.NOT. exst) then
           write(fname2(1:128),'(a)') localobsfile(1:il)
           localrec = obsrec
#ifdef SEAICE_DEBUG
           print *,'localrec ', localrec
           print *,'not exist'
#endif
        endif

        if ( localrec .GT. 0 ) then

#ifdef SEAICE_DEBUG
          print *,'calling mdsreadfile',fname2,localrec
#endif

          CALL READ_REC_3D_RL( fname2, cost_iprec, nnzobs,
     &                         localobs, localrec, 1, myThid )
        else
          do bj = jtlo,jthi
            do bi = itlo,ithi
              do k = 1,nnzobs
                do j = jmin,jmax
                  do i = imin,imax
                     localobs(i,j,k,bi,bj) = spval
                  enddo
                enddo
              enddo
            enddo
          enddo
        endif
cnew)

#ifdef SEAICE_DEBUG
          do bj = jtlo,jthi
            do bi = itlo,ithi
              do k = 1,nnzobs
                do i = imin,imax
                  do j = jmin,jmax
                    if (localobs(i,j,k,bi,bj) .LT. -1) THEN
                      print *,'obs rec date: ', -localobs(i,j,1,bi,bj)
                    endif
                  enddo
                enddo
              enddo
            enddo
          enddo
#endif

        do bj = jtlo,jthi
          do bi = itlo,ithi

            localcost    = 0. _d 0

c--           Determine the mask on weights
            do k = 1,nnzobs
             do j = jmin,jmax
              do i = imin,imax
               cmask(i,j,k) = cosphi(i,j,bi,bj)*localmask(i,j,k,bi,bj)
                if ( localobs(i,j,k,bi,bj) .lt. spminloc .or.
     &               localobs(i,j,k,bi,bj) .gt. spmaxloc .or.
     &               localobs(i,j,k,bi,bj) .eq. spzeroloc ) then
                   cmask(i,j,k) = 0. _d 0
                endif
              enddo
             enddo
            enddo
c--
            do k = 1,nnzobs
             do j = jmin,jmax
              do i = imin,imax
                localwww  = localweight(i,j,bi,bj)*cmask(i,j,k)

c only accumulate cost if there is ice observed but not simulated..
                if ( localobs(i,j,k,bi,bj) .GT. 0.0 .AND.
     &                areabar(i,j,1,bi,bj) .LE. 0.0) then

c                if ( localobs(i,j,k,bi,bj) .GT.
c     &               areabar(i,j,1,bi,bj)) then

                   junk = ( localbar(i,j,k,bi,bj) - SEAICE_clamp_salt )

c                   junk = localbar(i,j,k,bi,bj) -
c     &                         ( localbar(i,j,k,bi,bj) - 1.0)
                else
                   junk = 0.0
                endif

                localcost = localcost + junk*junk*localwww

#ifdef SEAICE_DEBUG
                if ((i == SEAICE_debugPointX) .and.
     &              (j == SEAICE_debugPointY)) then

                   print '(A,2i4,3(1x,1P2E15.3))',
     &                 'costg i j sbar, abar,obs     ',i,j,
     &                 localbar(i,j,k,bi,bj),
     &                 areabar(i,j,k,bi,bj),
     &                 localobs(i,j,k,bi,bj)

                   print '(A,2i4,2(1x,1P2E15.3))',
     &                 'costg i j bar-obs,wgt,loCost ',i,j,
     &                 junk,
     &                 localwww,
     &                 localcost
                endif
#endif

                if ( localwww .ne. 0. )
     &               num_local(bi,bj) = num_local(bi,bj) + 1. _d 0
              enddo
             enddo
            enddo

            objf_local(bi,bj) = objf_local(bi,bj) + localcost

          enddo !/bj
        enddo !/ bi

      enddo
c--   End of second loop over records.

c--   End of mult_local or localobsfile
      endif

#endif /* ALLOW_SEAICE_COST_SMR_AREA */
#endif /* ifdef ALLOW_COST */

      RETURN
      END
