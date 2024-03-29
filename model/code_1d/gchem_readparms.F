C $Header: /u/gcmpack/MITgcm/pkg/gchem/gchem_readparms.F,v 1.22 2017/08/09 15:23:37 mlosch Exp $
C $Name:  $

#include "GCHEM_OPTIONS.h"

CBOP
C !ROUTINE: GCHEM_READPARMS

C !INTERFACE: ==========================================================
      SUBROUTINE GCHEM_READPARMS( myThid )

C !DESCRIPTION:
C     Initialize GCHEM parameters, read in data.gchem

C !USES: ===============================================================
      IMPLICIT NONE
#include "SIZE.h"
#include "EEPARAMS.h"
#include "PARAMS.h"
#include "GCHEM.h"

C !INPUT PARAMETERS: ===================================================
C  myThid               :: thread number
      INTEGER myThid

C !OUTPUT PARAMETERS: ==================================================
C  none

#ifdef ALLOW_GCHEM

C !LOCAL VARIABLES: ====================================================
C  tIter0               :: retired parameter
C  iTracer              :: loop indices
C  iUnit                :: unit number for I/O
C  msgBuf               :: message buffer
      INTEGER tIter0
      INTEGER iUnit
      CHARACTER*(MAX_LEN_MBUF) msgBuf
CEOP

C- Sub-package on/off flags: not fully implemented, requires
C  to test the flag before any corresponding pkg S/R call

      NAMELIST /GCHEM_PARM01/
     &                   nsubtime,
     &                   useCFC,
     &                   useDIC,
     &                   useCFC,
     &                   useFGM, useBIMAP, useREcoM,
     &                   useBLING,
     &                   useDARWIN,
     &                   Filename1,
     &                   Filename2,
     &                   Filename3,
     &                   Filename4,
     &                   Filename5,
     &           gchem_int1, gchem_int2, gchem_int3,
     &           gchem_int4, gchem_int5,
     &           gchem_rl1, gchem_rl2, gchem_rl3,
     &           gchem_rl4, gchem_rl5,
     &           gchem_ForcingPeriod, gchem_ForcingCycle,
     &           tIter0

C---+----1----+----2----+----3----+----4----+----5----+----6----+----7-|--+----|

      IF ( .NOT.useGCHEM ) THEN
C-    pkg GCHEM is not used
        _BEGIN_MASTER(myThid)
C-    Track pkg activation status:
C     print a (weak) warning if data.gchem is found
         CALL PACKAGES_UNUSED_MSG( 'useGCHEM', ' ', ' ' )
        _END_MASTER(myThid)
        RETURN
      ENDIF

      _BEGIN_MASTER(myThid)

C Set defaults values for parameters in GCHEM.h
       useCFC = .FALSE.
       useDIC = .FALSE.
       useBLING  = .FALSE.
       useDARWIN = .FALSE.
       tIter0 = UNSET_I
       nsubtime=1
       Filename1=' '
       Filename2=' '
       Filename3=' '
       Filename4=' '
       Filename5=' '
       gchem_int1=0
       gchem_int2=0
       gchem_int3=0
       gchem_int4=0
       gchem_int5=0
       gchem_rl1=0. _d 0
       gchem_rl2=0. _d 0
       gchem_rl3=0. _d 0
       gchem_rl4=0. _d 0
       gchem_rl5=0. _d 0
c default periodic forcing to same as for physics
       gchem_ForcingPeriod=externForcingPeriod
       gchem_ForcingCycle=externForcingCycle
C Open and read the data.gchem file
      WRITE(msgBuf,'(A)') ' GCHEM_READPARMS: opening data.gchem'
      CALL PRINT_MESSAGE(msgBuf, standardMessageUnit,
     &                   SQUEEZE_RIGHT , 1)
      CALL OPEN_COPY_DATA_FILE(
     I                   'data.gchem', 'GCHEM_PARM01',
     O                   iUnit,
     I                   myThid )
      READ(UNIT=iUnit,NML=GCHEM_PARM01)
      WRITE(msgBuf,'(A)')
     &  ' GCHEM_READPARMS: finished reading data.gchem'
      CALL PRINT_MESSAGE(msgBuf, standardMessageUnit,
     &                   SQUEEZE_RIGHT , 1)

C Close the open data file
#ifdef SINGLE_DISK_IO
      CLOSE(iUnit)
#else
      CLOSE(iUnit,STATUS='DELETE')
#endif /* SINGLE_DISK_IO */

C- Check for retired parameters:
      IF ( tIter0 .NE. UNSET_I ) THEN
c      nRetired = nRetired+1
       WRITE(msgBuf,'(A,A)')
     &  'S/R GCHEM_READPARMS: Paramater "tIter0" is',
     &  ' no longer allowed in file "data.gchem"'
       CALL PRINT_ERROR( msgBuf , myThid)
       WRITE(msgBuf,'(A,A)')
     &  'S/R GCHEM_READPARMS: "tIter0" has been moved to',
     &  ' PTRACERS_Iter0 in file "data.ptracers".'
       CALL PRINT_ERROR( msgBuf , myThid)
       STOP 'ABNORMAL END: S/R GCHEM_READPARMS'
      ENDIF

      _END_MASTER(myThid)

C Everyone else must wait for the parameters to be loaded
      _BARRIER

#ifdef ALLOW_CFC
      IF ( useCFC ) THEN
        CALL CFC_READPARMS(myThid)
      ENDIF
#endif

#ifdef ALLOW_DIC
      IF ( useDIC ) THEN
        CALL DIC_READPARMS(myThid)
      ENDIF
#endif

#ifdef ALLOW_BLING
      IF ( useBLING ) THEN
        CALL BLING_READPARMS(myThid)
      ENDIF
#endif

#ifdef ALLOW_FGM
      IF ( useFGM ) CALL FGM_READPARMS( myThid )
#endif /* ALLOW_FGM */

#ifdef ALLOW_BIMAP
      IF ( useBIMAP ) CALL BIMAP_READPARMS( myThid )
#endif /* ALLOW_BIMAP */

#ifdef ALLOW_RECOM
      IF ( useREcoM ) CALL RECOM_READPARMS( myThid )
#endif /* ALLOW_RECOM */

#ifdef ALLOW_DARWIN
      IF ( useDARWIN ) THEN
        CALL DARWIN_READPARMS(myThid)
      ENDIF
#endif

#endif /* ALLOW_GCHEM */

      RETURN
      END
