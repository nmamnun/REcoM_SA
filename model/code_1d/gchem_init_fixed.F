C $Header: /u/gcmpack/MITgcm/pkg/gchem/gchem_init_fixed.F,v 1.12 2016/05/23 13:09:31 jmc Exp $
C $Name:  $

#include "GCHEM_OPTIONS.h"

C !INTERFACE: ==========================================================
      SUBROUTINE GCHEM_INIT_FIXED(myThid )

C !DESCRIPTION:
C calls subroutines that initialized fixed variables for any tracer
C experiment

C !USES: ===============================================================
      IMPLICIT NONE
#include "SIZE.h"
#include "EEPARAMS.h"
#include "PARAMS.h"
#include "GCHEM.h"

C !INPUT PARAMETERS: ===================================================
C  myThid               :: thread number
      INTEGER myThid
CEOP

#ifdef ALLOW_GCHEM

C     !LOCAL VARIABLES:

C jmc: simpler to put MASTER thread directive within individual S/R :
C      that leave the choice, for each S/R, to do either single (master)
C      thread tasks or Multi-threaded tasks.
c        _BEGIN_MASTER( myThid )
ccccccccccccccccccccccccccc
c initialize parameters   c
ccccccccccccccccccccccccccc
#ifdef ALLOW_CFC
      IF ( useCFC ) THEN
         print*,'QQ start cfc params'
         CALL CFC_PARAM( myThid )
         print*,'QQ read cfc atmos data'
         CALL CFC_ATMOS( myThid )
      ENDIF
#endif /* ALLOW_CFC */
#ifdef ALLOW_DIC
      IF ( useDIC ) THEN
         print*,'QQ load dic parameters, initial fixed'
         CALL DIC_INIT_FIXED( myThid )
      ENDIF
#endif /* ALLOW_DIC */
#ifdef ALLOW_BLING
      IF ( useBLING ) THEN
         CALL BLING_INIT_FIXED( myThid )
      ENDIF
#endif /* ALLOW_BLING */
c         _END_MASTER( myThid )

#ifdef ALLOW_RECOM
      IF ( useREcoM ) CALL RECOM_INIT_FIXED( myThid )
#endif /* ALLOW_RECOM */

#ifdef ALLOW_DARWIN
      IF ( useDARWIN ) THEN
         CALL DARWIN_INIT_FIXED(myThid)
      ENDIF
#endif

#ifdef ALLOW_DIAGNOSTICS
C     Define diagnostics Names :
      IF ( useDiagnostics ) THEN
        CALL GCHEM_DIAGNOSTICS_INIT( myThid )
      ENDIF
#endif /* ALLOW_DIAGNOSTICS */

#endif /* ALLOW_GCHEM */

      RETURN
      END
