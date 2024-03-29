#include "SEAICE_OPTIONS.h"
#ifdef ALLOW_CTRL
# include "CTRL_OPTIONS.h"
#endif

CBOP
C     !ROUTINE: seaice_ctrl_map_ini
C     !INTERFACE:
      subroutine seaice_ctrl_map_ini( mythid )

C     !DESCRIPTION: \bv
c     *=================================================================
c     | SUBROUTINE seaice_ctrl_map_ini
c     | Add the temperature, salinity, and diffusivity parts of the
c     | control vector to the model state and update the tile halos.
c     | The control vector is defined in the header file "ctrl.h".
c     *=================================================================
C     \ev

C     !USES:
      implicit none

c     == global variables ==
#include "SIZE.h"
#include "EEPARAMS.h"
#include "PARAMS.h"
#include "GRID.h"
#include "DYNVARS.h"
#include "FFIELDS.h"
#include "SEAICE_SIZE.h"
#include "SEAICE.h"
#ifdef ALLOW_CTRL
# include "CTRL_SIZE.h"
# include "ctrl.h"
# include "ctrl_dummy.h"
# include "optim.h"
#endif

C     !INPUT/OUTPUT PARAMETERS:
c     == routine arguments ==
      integer mythid

#ifdef ALLOW_CTRL
C     !LOCAL VARIABLES:
c     == local variables ==

      integer bi,bj
      integer i,j,k
      integer itlo,ithi
      integer jtlo,jthi
      integer jmin,jmax
      integer imin,imax
      integer il

      logical equal
      logical doglobalread
      logical ladinit

      character*( 80)   fnamegeneric

      _RL     fac
      _RL     tmpfld2d(1-olx:snx+olx,1-oly:sny+oly,nsx,nsy)

c     == external ==
      integer  ilnblnk
      external ilnblnk

c     == end of interface ==
CEOP

      jtlo = mybylo(mythid)
      jthi = mybyhi(mythid)
      itlo = mybxlo(mythid)
      ithi = mybxhi(mythid)
      jmin = 1
      jmax = sny
      imin = 1
      imax = snx

      doglobalread = .false.
      ladinit      = .false.

      equal = .true.

      if ( equal ) then
        fac = 1. _d 0
      else
        fac = 0. _d 0
      endif

      do bj = jtlo,jthi
        do bi = itlo,ithi
          do j = 1-oly,sny+oly
            do i = 1-olx,snx+olx
              tmpfld2d(i,j,bi,bj) = 0. _d 0
            enddo
          enddo
        enddo
      enddo

#ifdef ALLOW_SIAREA_CONTROL
c--   siarea.
      il=ilnblnk( xx_siarea_file )
      write(fnamegeneric(1:80),'(2a,i10.10)')
     &     xx_siarea_file(1:il),'.',optimcycle
      call active_read_xy( fnamegeneric, tmpfld2d, 1,
     &                      doglobalread, ladinit, optimcycle,
     &                      mythid, xx_siarea_dummy )
      do bj = jtlo,jthi
        do bi = itlo,ithi
            do j = jmin,jmax
              do i = imin,imax
                area(i,j,bi,bj) = area(i,j,bi,bj) +
     &                            tmpfld2d(i,j,bi,bj)
              enddo
            enddo
        enddo
      enddo
#endif

#ifdef ALLOW_SIHEFF_CONTROL
c--   siheff.
      il=ilnblnk( xx_siheff_file )
      write(fnamegeneric(1:80),'(2a,i10.10)')
     &     xx_siheff_file(1:il),'.',optimcycle
      call active_read_xy( fnamegeneric, tmpfld2d, 1,
     &                      doglobalread, ladinit, optimcycle,
     &                      mythid, xx_siheff_dummy )
      do bj = jtlo,jthi
        do bi = itlo,ithi
            do j = jmin,jmax
              do i = imin,imax
                heff(i,j,bi,bj) = heff(i,j,bi,bj) +
     &                            tmpfld2d(i,j,bi,bj)
              enddo
            enddo
        enddo
      enddo
#endif

#ifdef ALLOW_SIHSNOW_CONTROL
c--   sihsnow.
      il=ilnblnk( xx_sihsnow_file )
      write(fnamegeneric(1:80),'(2a,i10.10)')
     &     xx_sihsnow_file(1:il),'.',optimcycle
      call active_read_xy( fnamegeneric, tmpfld2d, 1,
     &                      doglobalread, ladinit, optimcycle,
     &                      mythid, xx_sihsnow_dummy )
      do bj = jtlo,jthi
        do bi = itlo,ithi
            do j = jmin,jmax
              do i = imin,imax
                hsnow(i,j,bi,bj) = hsnow(i,j,bi,bj) +
     &                             tmpfld2d(i,j,bi,bj)
              enddo
            enddo
        enddo
      enddo
#endif

c--   Update the tile edges.

#ifdef ALLOW_SIAREA_CONTROL
      _EXCH_XY_RL( area, mythid )
#endif

#ifdef ALLOW_SIHEFF_CONTROL
      _EXCH_XY_RL( heff, mythid )
#endif

#ifdef ALLOW_SIHSNOW_CONTROL
      _EXCH_XY_RL( hsnow, mythid )
#endif

#endif /* ALLOW_CTRL */

      return
      end
