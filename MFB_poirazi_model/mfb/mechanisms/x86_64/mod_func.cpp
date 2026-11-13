#include <stdio.h>
#include "hocdec.h"
extern int nrnmpi_myid;
extern int nrn_nobanner_;

extern "C" void _cad_reg(void);
extern "C" void _cagk_reg(void);
extern "C" void _calH_reg(void);
extern "C" void _cal_reg(void);
extern "C" void _car_reg(void);
extern "C" void _cat_reg(void);
extern "C" void _hha2_reg(void);
extern "C" void _hha_old_reg(void);
extern "C" void _h_reg(void);
extern "C" void _kadist_reg(void);
extern "C" void _kaprox_reg(void);
extern "C" void _kca_reg(void);
extern "C" void _km_reg(void);
extern "C" void _mfbsyn_reg(void);
extern "C" void _nap_reg(void);
extern "C" void _somacar_reg(void);

extern "C" void modl_reg() {
  if (!nrn_nobanner_) if (nrnmpi_myid < 1) {
    fprintf(stderr, "Additional mechanisms from files\n");
    fprintf(stderr, " \"./cad.mod\"");
    fprintf(stderr, " \"./cagk.mod\"");
    fprintf(stderr, " \"./calH.mod\"");
    fprintf(stderr, " \"./cal.mod\"");
    fprintf(stderr, " \"./car.mod\"");
    fprintf(stderr, " \"./cat.mod\"");
    fprintf(stderr, " \"./hha2.mod\"");
    fprintf(stderr, " \"./hha_old.mod\"");
    fprintf(stderr, " \"./h.mod\"");
    fprintf(stderr, " \"./kadist.mod\"");
    fprintf(stderr, " \"./kaprox.mod\"");
    fprintf(stderr, " \"./kca.mod\"");
    fprintf(stderr, " \"./km.mod\"");
    fprintf(stderr, " \"./mfbsyn.mod\"");
    fprintf(stderr, " \"./nap.mod\"");
    fprintf(stderr, " \"./somacar.mod\"");
    fprintf(stderr, "\n");
  }
  _cad_reg();
  _cagk_reg();
  _calH_reg();
  _cal_reg();
  _car_reg();
  _cat_reg();
  _hha2_reg();
  _hha_old_reg();
  _h_reg();
  _kadist_reg();
  _kaprox_reg();
  _kca_reg();
  _km_reg();
  _mfbsyn_reg();
  _nap_reg();
  _somacar_reg();
}
