/* Created by Language version: 7.7.0 */
/* NOT VECTORIZED */
#define NRN_VECTORIZED 0
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "mech_api.h"
#undef PI
#define nil 0
#define _pval pval
// clang-format off
#include "md1redef.h"
#include "section_fwd.hpp"
#include "nrniv_mf.h"
#include "md2redef.h"
#include "nrnconf.h"
// clang-format on
#include "neuron/cache/mechanism_range.hpp"
#include <vector>
using std::size_t;
static auto& std_cerr_stream = std::cerr;
static constexpr auto number_of_datum_variables = 4;
static constexpr auto number_of_floating_point_variables = 14;
namespace {
template <typename T>
using _nrn_mechanism_std_vector = std::vector<T>;
using _nrn_model_sorted_token = neuron::model_sorted_token;
using _nrn_mechanism_cache_range = neuron::cache::MechanismRange<number_of_floating_point_variables, number_of_datum_variables>;
using _nrn_mechanism_cache_instance = neuron::cache::MechanismInstance<number_of_floating_point_variables, number_of_datum_variables>;
using _nrn_non_owning_id_without_container = neuron::container::non_owning_identifier_without_container;
template <typename T>
using _nrn_mechanism_field = neuron::mechanism::field<T>;
template <typename... Args>
void _nrn_mechanism_register_data_fields(Args&&... args) {
  neuron::mechanism::register_data_fields(std::forward<Args>(args)...);
}
}
 
#if !NRNGPU
#undef exp
#define exp hoc_Exp
#if NRN_ENABLE_ARCH_INDEP_EXP_POW
#undef pow
#define pow hoc_pow
#endif
#endif
 
#define nrn_init _nrn_init__cat
#define _nrn_initial _nrn_initial__cat
#define nrn_cur _nrn_cur__cat
#define _nrn_current _nrn_current__cat
#define nrn_jacob _nrn_jacob__cat
#define nrn_state _nrn_state__cat
#define _net_receive _net_receive__cat 
#define rates rates__cat 
#define states states__cat 
 
#define _threadargscomma_ /**/
#define _threadargsprotocomma_ /**/
#define _internalthreadargsprotocomma_ /**/
#define _threadargs_ /**/
#define _threadargsproto_ /**/
#define _internalthreadargsproto_ /**/
 	/*SUPPRESS 761*/
	/*SUPPRESS 762*/
	/*SUPPRESS 763*/
	/*SUPPRESS 765*/
	 extern double *hoc_getarg(int);
 
#define t nrn_threads->_t
#define dt nrn_threads->_dt
#define gcatbar _ml->template fpfield<0>(_iml)
#define gcatbar_columnindex 0
#define iCa _ml->template fpfield<1>(_iml)
#define iCa_columnindex 1
#define minf _ml->template fpfield<2>(_iml)
#define minf_columnindex 2
#define hinf _ml->template fpfield<3>(_iml)
#define hinf_columnindex 3
#define taum _ml->template fpfield<4>(_iml)
#define taum_columnindex 4
#define tauh _ml->template fpfield<5>(_iml)
#define tauh_columnindex 5
#define m _ml->template fpfield<6>(_iml)
#define m_columnindex 6
#define h _ml->template fpfield<7>(_iml)
#define h_columnindex 7
#define cai _ml->template fpfield<8>(_iml)
#define cai_columnindex 8
#define cao _ml->template fpfield<9>(_iml)
#define cao_columnindex 9
#define Dm _ml->template fpfield<10>(_iml)
#define Dm_columnindex 10
#define Dh _ml->template fpfield<11>(_iml)
#define Dh_columnindex 11
#define gcat _ml->template fpfield<12>(_iml)
#define gcat_columnindex 12
#define _g _ml->template fpfield<13>(_iml)
#define _g_columnindex 13
#define _ion_cai *(_ml->dptr_field<0>(_iml))
#define _p_ion_cai static_cast<neuron::container::data_handle<double>>(_ppvar[0])
#define _ion_cao *(_ml->dptr_field<1>(_iml))
#define _p_ion_cao static_cast<neuron::container::data_handle<double>>(_ppvar[1])
#define _ion_iCa *(_ml->dptr_field<2>(_iml))
#define _p_ion_iCa static_cast<neuron::container::data_handle<double>>(_ppvar[2])
#define _ion_diCadv *(_ml->dptr_field<3>(_iml))
 static _nrn_mechanism_cache_instance _ml_real{nullptr};
static _nrn_mechanism_cache_range *_ml{&_ml_real};
static size_t _iml{0};
static Datum *_ppvar;
 static int hoc_nrnpointerindex =  -1;
 static Prop* _extcall_prop;
 /* _prop_id kind of shadows _extcall_prop to allow validity checking. */
 static _nrn_non_owning_id_without_container _prop_id{};
 /* external NEURON variables */
 extern double celsius;
 /* declaration of user functions */
 static void _hoc_KTF(void);
 static void _hoc_alpm(void);
 static void _hoc_alph(void);
 static void _hoc_betm(void);
 static void _hoc_beth(void);
 static void _hoc_efun(void);
 static void _hoc_ghk(void);
 static void _hoc_h2(void);
 static void _hoc_rates(void);
 static void _hoc_states(void);
 static int _mechtype;
extern void _nrn_cacheloop_reg(int, int);
extern void hoc_register_limits(int, HocParmLimits*);
extern void hoc_register_units(int, HocParmUnits*);
extern void nrn_promote(Prop*, int, int);
 
#define NMODL_TEXT 1
#if NMODL_TEXT
static void register_nmodl_text_and_filename(int mechtype);
#endif
 static void _hoc_setdata();
 /* connect user functions to hoc names */
 static VoidFunc hoc_intfunc[] = {
 {"setdata_cat", _hoc_setdata},
 {"KTF_cat", _hoc_KTF},
 {"alpm_cat", _hoc_alpm},
 {"alph_cat", _hoc_alph},
 {"betm_cat", _hoc_betm},
 {"beth_cat", _hoc_beth},
 {"efun_cat", _hoc_efun},
 {"ghk_cat", _hoc_ghk},
 {"h2_cat", _hoc_h2},
 {"rates_cat", _hoc_rates},
 {"states_cat", _hoc_states},
 {0, 0}
};
 
/* Direct Python call wrappers to density mechanism functions.*/
 static double _npy_KTF(Prop*);
 static double _npy_alpm(Prop*);
 static double _npy_alph(Prop*);
 static double _npy_betm(Prop*);
 static double _npy_beth(Prop*);
 static double _npy_efun(Prop*);
 static double _npy_ghk(Prop*);
 static double _npy_h2(Prop*);
 static double _npy_rates(Prop*);
 static double _npy_states(Prop*);
 
static NPyDirectMechFunc npy_direct_func_proc[] = {
 {"KTF", _npy_KTF},
 {"alpm", _npy_alpm},
 {"alph", _npy_alph},
 {"betm", _npy_betm},
 {"beth", _npy_beth},
 {"efun", _npy_efun},
 {"ghk", _npy_ghk},
 {"h2", _npy_h2},
 {"rates", _npy_rates},
 {"states", _npy_states},
 {0, 0}
};
#define KTF KTF_cat
#define _f_betm _f_betm_cat
#define _f_alpm _f_alpm_cat
#define _f_beth _f_beth_cat
#define _f_alph _f_alph_cat
#define alpm alpm_cat
#define alph alph_cat
#define betm betm_cat
#define beth beth_cat
#define efun efun_cat
#define ghk ghk_cat
#define h2 h2_cat
 extern double KTF( double );
 extern double _f_betm( double );
 extern double _f_alpm( double );
 extern double _f_beth( double );
 extern double _f_alph( double );
 extern double alpm( double );
 extern double alph( double );
 extern double betm( double );
 extern double beth( double );
 extern double efun( double );
 extern double ghk( double , double , double );
 extern double h2( double );
 /* declare global and static user variables */
 #define gind 0
 #define _gth 0
#define eca eca_cat
 double eca = 140;
#define ki ki_cat
 double ki = 0.001;
#define tfi tfi_cat
 double tfi = 0.68;
#define tfa tfa_cat
 double tfa = 1;
#define tBase tBase_cat
 double tBase = 23.5;
#define usetable usetable_cat
 double usetable = 1;
 /* some parameters have upper and lower limits */
 static HocParmLimits _hoc_parm_limits[] = {
 {"usetable_cat", 0, 1},
 {0, 0, 0}
};
 static HocParmUnits _hoc_parm_units[] = {
 {"tBase_cat", "degC"},
 {"ki_cat", "mM"},
 {"gcatbar_cat", "mho/cm2"},
 {"iCa_cat", "mA/cm2"},
 {0, 0}
};
 static double delta_t = 0.01;
 static double h0 = 0;
 static double m0 = 0;
 static double v = 0;
 /* connect global user variables to hoc */
 static DoubScal hoc_scdoub[] = {
 {"tBase_cat", &tBase_cat},
 {"ki_cat", &ki_cat},
 {"tfa_cat", &tfa_cat},
 {"tfi_cat", &tfi_cat},
 {"eca_cat", &eca_cat},
 {"usetable_cat", &usetable_cat},
 {0, 0}
};
 static DoubVec hoc_vdoub[] = {
 {0, 0, 0}
};
 static double _sav_indep;
 extern void _nrn_setdata_reg(int, void(*)(Prop*));
 static void _setdata(Prop* _prop) {
 _extcall_prop = _prop;
 _prop_id = _nrn_get_prop_id(_prop);
 neuron::legacy::set_globals_from_prop(_prop, _ml_real, _ml, _iml);
_ppvar = _nrn_mechanism_access_dparam(_prop);
 Node * _node = _nrn_mechanism_access_node(_prop);
v = _nrn_mechanism_access_voltage(_node);
 }
 static void _hoc_setdata() {
 Prop *_prop, *hoc_getdata_range(int);
 _prop = hoc_getdata_range(_mechtype);
   _setdata(_prop);
 hoc_retpushx(1.);
}
 static void nrn_alloc(Prop*);
static void nrn_init(_nrn_model_sorted_token const&, NrnThread*, Memb_list*, int);
static void nrn_state(_nrn_model_sorted_token const&, NrnThread*, Memb_list*, int);
 static void nrn_cur(_nrn_model_sorted_token const&, NrnThread*, Memb_list*, int);
static void nrn_jacob(_nrn_model_sorted_token const&, NrnThread*, Memb_list*, int);
 
static int _ode_count(int);
 /* connect range variables in _p that hoc is supposed to know about */
 static const char *_mechanism[] = {
 "7.7.0",
"cat",
 "gcatbar_cat",
 0,
 "iCa_cat",
 "minf_cat",
 "hinf_cat",
 "taum_cat",
 "tauh_cat",
 0,
 "m_cat",
 "h_cat",
 0,
 0};
 static Symbol* _ca_sym;
 static Symbol* _Ca_sym;
 
 /* Used by NrnProperty */
 static _nrn_mechanism_std_vector<double> _parm_default{
     0, /* gcatbar */
 }; 
 
 
extern Prop* need_memb(Symbol*);
static void nrn_alloc(Prop* _prop) {
  Prop *prop_ion{};
  Datum *_ppvar{};
   _ppvar = nrn_prop_datum_alloc(_mechtype, 4, _prop);
    _nrn_mechanism_access_dparam(_prop) = _ppvar;
     _nrn_mechanism_cache_instance _ml_real{_prop};
    auto* const _ml = &_ml_real;
    size_t const _iml{};
    assert(_nrn_mechanism_get_num_vars(_prop) == 14);
 	/*initialize range parameters*/
 	gcatbar = _parm_default[0]; /* 0 */
 	 assert(_nrn_mechanism_get_num_vars(_prop) == 14);
 	_nrn_mechanism_access_dparam(_prop) = _ppvar;
 	/*connect ionic variables to this model*/
 prop_ion = need_memb(_ca_sym);
 nrn_promote(prop_ion, 1, 0);
 	_ppvar[0] = _nrn_mechanism_get_param_handle(prop_ion, 1); /* cai */
 	_ppvar[1] = _nrn_mechanism_get_param_handle(prop_ion, 2); /* cao */
 prop_ion = need_memb(_Ca_sym);
 	_ppvar[2] = _nrn_mechanism_get_param_handle(prop_ion, 3); /* iCa */
 	_ppvar[3] = _nrn_mechanism_get_param_handle(prop_ion, 4); /* _ion_diCadv */
 
}
 static void _initlists();
 extern Symbol* hoc_lookup(const char*);
extern void _nrn_thread_reg(int, int, void(*)(Datum*));
void _nrn_thread_table_reg(int, nrn_thread_table_check_t);
extern void hoc_register_tolerance(int, HocStateTolerance*, Symbol***);
extern void _cvode_abstol( Symbol**, double*, int);

 extern "C" void _cat_reg() {
	int _vectorized = 0;
  _initlists();
 	ion_reg("ca", -10000.);
 	ion_reg("Ca", 2.0);
 	_ca_sym = hoc_lookup("ca_ion");
 	_Ca_sym = hoc_lookup("Ca_ion");
 	register_mech(_mechanism, nrn_alloc,nrn_cur, nrn_jacob, nrn_state, nrn_init, hoc_nrnpointerindex, 0);
 _mechtype = nrn_get_mechtype(_mechanism[1]);
 hoc_register_parm_default(_mechtype, &_parm_default);
         hoc_register_npy_direct(_mechtype, npy_direct_func_proc);
     _nrn_setdata_reg(_mechtype, _setdata);
 #if NMODL_TEXT
  register_nmodl_text_and_filename(_mechtype);
#endif
   _nrn_mechanism_register_data_fields(_mechtype,
                                       _nrn_mechanism_field<double>{"gcatbar"} /* 0 */,
                                       _nrn_mechanism_field<double>{"iCa"} /* 1 */,
                                       _nrn_mechanism_field<double>{"minf"} /* 2 */,
                                       _nrn_mechanism_field<double>{"hinf"} /* 3 */,
                                       _nrn_mechanism_field<double>{"taum"} /* 4 */,
                                       _nrn_mechanism_field<double>{"tauh"} /* 5 */,
                                       _nrn_mechanism_field<double>{"m"} /* 6 */,
                                       _nrn_mechanism_field<double>{"h"} /* 7 */,
                                       _nrn_mechanism_field<double>{"cai"} /* 8 */,
                                       _nrn_mechanism_field<double>{"cao"} /* 9 */,
                                       _nrn_mechanism_field<double>{"Dm"} /* 10 */,
                                       _nrn_mechanism_field<double>{"Dh"} /* 11 */,
                                       _nrn_mechanism_field<double>{"gcat"} /* 12 */,
                                       _nrn_mechanism_field<double>{"_g"} /* 13 */,
                                       _nrn_mechanism_field<double*>{"_ion_cai", "ca_ion"} /* 0 */,
                                       _nrn_mechanism_field<double*>{"_ion_cao", "ca_ion"} /* 1 */,
                                       _nrn_mechanism_field<double*>{"_ion_iCa", "Ca_ion"} /* 2 */,
                                       _nrn_mechanism_field<double*>{"_ion_diCadv", "Ca_ion"} /* 3 */);
  hoc_register_prop_size(_mechtype, 14, 4);
  hoc_register_dparam_semantics(_mechtype, 0, "ca_ion");
  hoc_register_dparam_semantics(_mechtype, 1, "ca_ion");
  hoc_register_dparam_semantics(_mechtype, 2, "Ca_ion");
  hoc_register_dparam_semantics(_mechtype, 3, "Ca_ion");
 	hoc_register_cvode(_mechtype, _ode_count, 0, 0, 0);
 
    hoc_register_var(hoc_scdoub, hoc_vdoub, hoc_intfunc);
 	ivoc_help("help ?1 cat /home/nishant/lab/project_MFB/MFB_poirazi_model/mfb/mechanisms/cat.mod\n");
 hoc_register_limits(_mechtype, _hoc_parm_limits);
 hoc_register_units(_mechtype, _hoc_parm_units);
 }
 static double FARADAY = 96520.0;
 static double R = 8.3134;
 static double KTOMV = .0853;
 static double *_t_alph;
 static double *_t_beth;
 static double *_t_alpm;
 static double *_t_betm;
 static double _zfacm , _zfach ;
static int _reset;
static const char *modelname = "t-type calcium channel with high threshold for activation";

static int error;
static int _ninits = 0;
static int _match_recurse=1;
static void _modl_cleanup(){ _match_recurse=1;}
static int rates(double);
static int states();
 static double _n_betm(double);
 static double _n_alpm(double);
 static double _n_beth(double);
 static double _n_alph(double);
 
double h2 (  double _lcai ) {
   double _lh2;
 _lh2 = ki / ( ki + _lcai ) ;
   
return _lh2;
 }
 
static void _hoc_h2(void) {
  double _r;
    _r =  h2 (  *getarg(1) );
 hoc_retpushx(_r);
}
 
static double _npy_h2(Prop* _prop) {
    double _r{0.0};
    neuron::legacy::set_globals_from_prop(_prop, _ml_real, _ml, _iml);
  _ppvar = _nrn_mechanism_access_dparam(_prop);
 _r =  h2 (  *getarg(1) );
 return(_r);
}
 
double ghk (  double _lv , double _lci , double _lco ) {
   double _lghk;
 double _lnu , _lf ;
 _lf = KTF ( _threadargscomma_ celsius ) / 2.0 ;
   _lnu = _lv / _lf ;
   _lghk = - _lf * ( 1. - ( _lci / _lco ) * exp ( _lnu ) ) * efun ( _threadargscomma_ _lnu ) ;
   
return _lghk;
 }
 
static void _hoc_ghk(void) {
  double _r;
    _r =  ghk (  *getarg(1) , *getarg(2) , *getarg(3) );
 hoc_retpushx(_r);
}
 
static double _npy_ghk(Prop* _prop) {
    double _r{0.0};
    neuron::legacy::set_globals_from_prop(_prop, _ml_real, _ml, _iml);
  _ppvar = _nrn_mechanism_access_dparam(_prop);
 _r =  ghk (  *getarg(1) , *getarg(2) , *getarg(3) );
 return(_r);
}
 
double KTF (  double _lcelsius ) {
   double _lKTF;
 _lKTF = ( ( 25. / 293.15 ) * ( _lcelsius + 273.15 ) ) ;
   
return _lKTF;
 }
 
static void _hoc_KTF(void) {
  double _r;
    _r =  KTF (  *getarg(1) );
 hoc_retpushx(_r);
}
 
static double _npy_KTF(Prop* _prop) {
    double _r{0.0};
    neuron::legacy::set_globals_from_prop(_prop, _ml_real, _ml, _iml);
  _ppvar = _nrn_mechanism_access_dparam(_prop);
 _r =  KTF (  *getarg(1) );
 return(_r);
}
 
double efun (  double _lz ) {
   double _lefun;
 if ( fabs ( _lz ) < 1e-4 ) {
     _lefun = 1.0 - _lz / 2.0 ;
     }
   else {
     _lefun = _lz / ( exp ( _lz ) - 1.0 ) ;
     }
   
return _lefun;
 }
 
static void _hoc_efun(void) {
  double _r;
    _r =  efun (  *getarg(1) );
 hoc_retpushx(_r);
}
 
static double _npy_efun(Prop* _prop) {
    double _r{0.0};
    neuron::legacy::set_globals_from_prop(_prop, _ml_real, _ml, _iml);
  _ppvar = _nrn_mechanism_access_dparam(_prop);
 _r =  efun (  *getarg(1) );
 return(_r);
}
 static double _mfac_alph, _tmin_alph;
 static void _check_alph();
 static void _check_alph() {
  static int _maktable=1; int _i, _j, _ix = 0;
  double _xi, _tmax;
  if (!usetable) {return;}
  if (_maktable) { double _x, _dx; _maktable=0;
   _tmin_alph =  - 150.0 ;
   _tmax =  150.0 ;
   _dx = (_tmax - _tmin_alph)/200.; _mfac_alph = 1./_dx;
   for (_i=0, _x=_tmin_alph; _i < 201; _x += _dx, _i++) {
    _t_alph[_i] = _f_alph(_x);
   }
  }
 }

 double alph(double _lv){ _check_alph();
 return _n_alph(_lv);
 }

 static double _n_alph(double _lv){ int _i, _j;
 double _xi, _theta;
 if (!usetable) {
 return _f_alph(_lv); 
}
 _xi = _mfac_alph * (_lv - _tmin_alph);
 if (std::isnan(_xi)) {
  return _xi; }
 if (_xi <= 0.) {
 return _t_alph[0];
 }
 if (_xi >= 200.) {
 return _t_alph[200];
 }
 _i = (int) _xi;
 return _t_alph[_i] + (_xi - (double)_i)*(_t_alph[_i+1] - _t_alph[_i]);
 }

 
double _f_alph (  double _lv ) {
   double _lalph;
 _lalph = 1.6e-4 * exp ( - ( _lv + 57.0 ) / 19.0 ) ;
   
return _lalph;
 }
 
static void _hoc_alph(void) {
  double _r;
     _r =  alph (  *getarg(1) );
 hoc_retpushx(_r);
}
 
static double _npy_alph(Prop* _prop) {
    double _r{0.0};
    neuron::legacy::set_globals_from_prop(_prop, _ml_real, _ml, _iml);
  _ppvar = _nrn_mechanism_access_dparam(_prop);
  _r =  alph (  *getarg(1) );
 return(_r);
}
 static double _mfac_beth, _tmin_beth;
 static void _check_beth();
 static void _check_beth() {
  static int _maktable=1; int _i, _j, _ix = 0;
  double _xi, _tmax;
  if (!usetable) {return;}
  if (_maktable) { double _x, _dx; _maktable=0;
   _tmin_beth =  - 150.0 ;
   _tmax =  150.0 ;
   _dx = (_tmax - _tmin_beth)/200.; _mfac_beth = 1./_dx;
   for (_i=0, _x=_tmin_beth; _i < 201; _x += _dx, _i++) {
    _t_beth[_i] = _f_beth(_x);
   }
  }
 }

 double beth(double _lv){ _check_beth();
 return _n_beth(_lv);
 }

 static double _n_beth(double _lv){ int _i, _j;
 double _xi, _theta;
 if (!usetable) {
 return _f_beth(_lv); 
}
 _xi = _mfac_beth * (_lv - _tmin_beth);
 if (std::isnan(_xi)) {
  return _xi; }
 if (_xi <= 0.) {
 return _t_beth[0];
 }
 if (_xi >= 200.) {
 return _t_beth[200];
 }
 _i = (int) _xi;
 return _t_beth[_i] + (_xi - (double)_i)*(_t_beth[_i+1] - _t_beth[_i]);
 }

 
double _f_beth (  double _lv ) {
   double _lbeth;
 _lbeth = 1.0 / ( exp ( ( - _lv + 15.0 ) / 10.0 ) + 1.0 ) ;
   
return _lbeth;
 }
 
static void _hoc_beth(void) {
  double _r;
     _r =  beth (  *getarg(1) );
 hoc_retpushx(_r);
}
 
static double _npy_beth(Prop* _prop) {
    double _r{0.0};
    neuron::legacy::set_globals_from_prop(_prop, _ml_real, _ml, _iml);
  _ppvar = _nrn_mechanism_access_dparam(_prop);
  _r =  beth (  *getarg(1) );
 return(_r);
}
 static double _mfac_alpm, _tmin_alpm;
 static void _check_alpm();
 static void _check_alpm() {
  static int _maktable=1; int _i, _j, _ix = 0;
  double _xi, _tmax;
  if (!usetable) {return;}
  if (_maktable) { double _x, _dx; _maktable=0;
   _tmin_alpm =  - 150.0 ;
   _tmax =  150.0 ;
   _dx = (_tmax - _tmin_alpm)/200.; _mfac_alpm = 1./_dx;
   for (_i=0, _x=_tmin_alpm; _i < 201; _x += _dx, _i++) {
    _t_alpm[_i] = _f_alpm(_x);
   }
  }
 }

 double alpm(double _lv){ _check_alpm();
 return _n_alpm(_lv);
 }

 static double _n_alpm(double _lv){ int _i, _j;
 double _xi, _theta;
 if (!usetable) {
 return _f_alpm(_lv); 
}
 _xi = _mfac_alpm * (_lv - _tmin_alpm);
 if (std::isnan(_xi)) {
  return _xi; }
 if (_xi <= 0.) {
 return _t_alpm[0];
 }
 if (_xi >= 200.) {
 return _t_alpm[200];
 }
 _i = (int) _xi;
 return _t_alpm[_i] + (_xi - (double)_i)*(_t_alpm[_i+1] - _t_alpm[_i]);
 }

 
double _f_alpm (  double _lv ) {
   double _lalpm;
 _lalpm = 0.1967 * ( - 1.0 * _lv + 19.88 ) / ( exp ( ( - 1.0 * _lv + 19.88 ) / 10.0 ) - 1.0 ) ;
   
return _lalpm;
 }
 
static void _hoc_alpm(void) {
  double _r;
     _r =  alpm (  *getarg(1) );
 hoc_retpushx(_r);
}
 
static double _npy_alpm(Prop* _prop) {
    double _r{0.0};
    neuron::legacy::set_globals_from_prop(_prop, _ml_real, _ml, _iml);
  _ppvar = _nrn_mechanism_access_dparam(_prop);
  _r =  alpm (  *getarg(1) );
 return(_r);
}
 static double _mfac_betm, _tmin_betm;
 static void _check_betm();
 static void _check_betm() {
  static int _maktable=1; int _i, _j, _ix = 0;
  double _xi, _tmax;
  if (!usetable) {return;}
  if (_maktable) { double _x, _dx; _maktable=0;
   _tmin_betm =  - 150.0 ;
   _tmax =  150.0 ;
   _dx = (_tmax - _tmin_betm)/200.; _mfac_betm = 1./_dx;
   for (_i=0, _x=_tmin_betm; _i < 201; _x += _dx, _i++) {
    _t_betm[_i] = _f_betm(_x);
   }
  }
 }

 double betm(double _lv){ _check_betm();
 return _n_betm(_lv);
 }

 static double _n_betm(double _lv){ int _i, _j;
 double _xi, _theta;
 if (!usetable) {
 return _f_betm(_lv); 
}
 _xi = _mfac_betm * (_lv - _tmin_betm);
 if (std::isnan(_xi)) {
  return _xi; }
 if (_xi <= 0.) {
 return _t_betm[0];
 }
 if (_xi >= 200.) {
 return _t_betm[200];
 }
 _i = (int) _xi;
 return _t_betm[_i] + (_xi - (double)_i)*(_t_betm[_i+1] - _t_betm[_i]);
 }

 
double _f_betm (  double _lv ) {
   double _lbetm;
 _lbetm = 0.046 * exp ( - _lv / 22.73 ) ;
   
return _lbetm;
 }
 
static void _hoc_betm(void) {
  double _r;
     _r =  betm (  *getarg(1) );
 hoc_retpushx(_r);
}
 
static double _npy_betm(Prop* _prop) {
    double _r{0.0};
    neuron::legacy::set_globals_from_prop(_prop, _ml_real, _ml, _iml);
  _ppvar = _nrn_mechanism_access_dparam(_prop);
  _r =  betm (  *getarg(1) );
 return(_r);
}
 
static int  states (  ) {
   rates ( _threadargscomma_ v ) ;
   m = m + _zfacm * ( minf - m ) ;
   h = h + _zfach * ( hinf - h ) ;
   
/*VERBATIM*/
        return 0;
  return 0; }
 
static void _hoc_states(void) {
  double _r;
  
  if(!_prop_id) {
    hoc_execerror("No data for states_cat. Requires prior call to setdata_cat and that the specified mechanism instance still be in existence.", NULL);
  } else {
    _setdata(_extcall_prop);
  }
   _r = 1.;
 states (  );
 hoc_retpushx(_r);
}
 
static double _npy_states(Prop* _prop) {
    double _r{0.0};
    neuron::legacy::set_globals_from_prop(_prop, _ml_real, _ml, _iml);
  _ppvar = _nrn_mechanism_access_dparam(_prop);
 _r = 1.;
 states (  );
 return(_r);
}
 
static int  rates (  double _lv ) {
   double _la ;
 _la = alpm ( _threadargscomma_ _lv ) ;
   taum = 1.0 / ( tfa * ( _la + betm ( _threadargscomma_ _lv ) ) ) ;
   minf = _la / ( _la + betm ( _threadargscomma_ _lv ) ) ;
   _zfacm = ( 1.0 - exp ( - dt / taum ) ) ;
   _la = alph ( _threadargscomma_ _lv ) ;
   tauh = 1.0 / ( tfi * ( _la + beth ( _threadargscomma_ _lv ) ) ) ;
   hinf = _la / ( _la + beth ( _threadargscomma_ _lv ) ) ;
   _zfach = ( 1.0 - exp ( - dt / tauh ) ) ;
    return 0; }
 
static void _hoc_rates(void) {
  double _r;
  
  if(!_prop_id) {
    hoc_execerror("No data for rates_cat. Requires prior call to setdata_cat and that the specified mechanism instance still be in existence.", NULL);
  } else {
    _setdata(_extcall_prop);
  }
   _r = 1.;
 rates (  *getarg(1) );
 hoc_retpushx(_r);
}
 
static double _npy_rates(Prop* _prop) {
    double _r{0.0};
    neuron::legacy::set_globals_from_prop(_prop, _ml_real, _ml, _iml);
  _ppvar = _nrn_mechanism_access_dparam(_prop);
 _r = 1.;
 rates (  *getarg(1) );
 return(_r);
}
 
static int _ode_count(int _type){ hoc_execerror("cat", "cannot be used with CVODE"); return 0;}

static void initmodel() {
  int _i; double _save;_ninits++;
 _save = t;
 t = 0.0;
{
  h = h0;
  m = m0;
 {
   rates ( _threadargscomma_ v ) ;
   m = minf ;
   h = hinf ;
   gcat = gcatbar * m * m * h * h2 ( _threadargscomma_ cai ) ;
   }
  _sav_indep = t; t = _save;

}
}

static void nrn_init(_nrn_model_sorted_token const& _sorted_token, NrnThread* _nt, Memb_list* _ml_arg, int _type){
Node *_nd; double _v; int* _ni; int _cntml;
_nrn_mechanism_cache_range _lmr{_sorted_token, *_nt, *_ml_arg, _type};
auto* const _vec_v = _nt->node_voltage_storage();
_ml = &_lmr;
_ni = _ml_arg->_nodeindices;
_cntml = _ml_arg->_nodecount;
for (_iml = 0; _iml < _cntml; ++_iml) {
 _ppvar = _ml_arg->_pdata[_iml];
   _v = _vec_v[_ni[_iml]];
 v = _v;
  cai = _ion_cai;
  cao = _ion_cao;
 initmodel();
 }}

static double _nrn_current(double _v){double _current=0.;v=_v;{ {
   gcat = gcatbar * m * m * h * h2 ( _threadargscomma_ cai ) ;
   iCa = gcat * ghk ( _threadargscomma_ v , cai , cao ) ;
   }
 _current += iCa;

} return _current;
}

static void nrn_cur(_nrn_model_sorted_token const& _sorted_token, NrnThread* _nt, Memb_list* _ml_arg, int _type){
_nrn_mechanism_cache_range _lmr{_sorted_token, *_nt, *_ml_arg, _type};
auto const _vec_rhs = _nt->node_rhs_storage();
auto const _vec_sav_rhs = _nt->node_sav_rhs_storage();
auto const _vec_v = _nt->node_voltage_storage();
Node *_nd; int* _ni; double _rhs, _v; int _cntml;
_ml = &_lmr;
_ni = _ml_arg->_nodeindices;
_cntml = _ml_arg->_nodecount;
for (_iml = 0; _iml < _cntml; ++_iml) {
 _ppvar = _ml_arg->_pdata[_iml];
   _v = _vec_v[_ni[_iml]];
  cai = _ion_cai;
  cao = _ion_cao;
 auto const _g_local = _nrn_current(_v + .001);
 	{ double _diCa;
  _diCa = iCa;
 _rhs = _nrn_current(_v);
  _ion_diCadv += (_diCa - iCa)/.001 ;
 	}
 _g = (_g_local - _rhs)/.001;
  _ion_iCa += iCa ;
	 _vec_rhs[_ni[_iml]] -= _rhs;
 
}}

static void nrn_jacob(_nrn_model_sorted_token const& _sorted_token, NrnThread* _nt, Memb_list* _ml_arg, int _type) {
_nrn_mechanism_cache_range _lmr{_sorted_token, *_nt, *_ml_arg, _type};
auto const _vec_d = _nt->node_d_storage();
auto const _vec_sav_d = _nt->node_sav_d_storage();
auto* const _ml = &_lmr;
Node *_nd; int* _ni; int _iml, _cntml;
_ni = _ml_arg->_nodeindices;
_cntml = _ml_arg->_nodecount;
for (_iml = 0; _iml < _cntml; ++_iml) {
  _vec_d[_ni[_iml]] += _g;
 
}}

static void nrn_state(_nrn_model_sorted_token const& _sorted_token, NrnThread* _nt, Memb_list* _ml_arg, int _type){
Node *_nd; double _v = 0.0; int* _ni; int _cntml;
_nrn_mechanism_cache_range _lmr{_sorted_token, *_nt, *_ml_arg, _type};
auto* const _vec_v = _nt->node_voltage_storage();
_ml = &_lmr;
_ni = _ml_arg->_nodeindices;
_cntml = _ml_arg->_nodecount;
for (_iml = 0; _iml < _cntml; ++_iml) {
 _ppvar = _ml_arg->_pdata[_iml];
 _nd = _ml_arg->_nodelist[_iml];
   _v = _vec_v[_ni[_iml]];
 v=_v;
{
  cai = _ion_cai;
  cao = _ion_cao;
 { error =  states();
 if(error){
  std_cerr_stream << "at line 60 in file cat.mod:\n	SOLVE states\n";
  std_cerr_stream << _ml << ' ' << _iml << '\n';
  abort_run(error);
}
 } }}

}

static void terminal(){}

static void _initlists() {
 int _i; static int _first = 1;
  if (!_first) return;
   _t_alph = makevector(201*sizeof(double));
   _t_beth = makevector(201*sizeof(double));
   _t_alpm = makevector(201*sizeof(double));
   _t_betm = makevector(201*sizeof(double));
_first = 0;
}

#if NMODL_TEXT
static void register_nmodl_text_and_filename(int mech_type) {
    const char* nmodl_filename = "/home/nishant/lab/project_MFB/MFB_poirazi_model/mfb/mechanisms/cat.mod";
    const char* nmodl_file_text = 
  "TITLE t-type calcium channel with high threshold for activation\n"
  ": used in somatic and dendritic regions \n"
  ": it calculates I_Ca using channel permeability instead of conductance\n"
  "\n"
  "UNITS {\n"
  "	(mA) = (milliamp)\n"
  "	(mV) = (millivolt)\n"
  "\n"
  "	FARADAY = 96520 (coul)\n"
  "	R = 8.3134 (joule/degK)\n"
  "	KTOMV = .0853 (mV/degC)\n"
  "}\n"
  "\n"
  "INDEPENDENT {t FROM 0 TO 1 WITH 1 (ms)}\n"
  "\n"
  "PARAMETER {           :parameters that can be entered when function is called in cell-setup \n"
  "        dt            (ms)\n"
  "	v             (mV)\n"
  "        tBase = 23.5  (degC)\n"
  "	celsius = 22  (degC)\n"
  "	gcatbar = 0   (mho/cm2)  : initialized conductance\n"
  "	ki = 0.001    (mM)\n"
  "	cai = 5.e-5   (mM)       : initial internal Ca++ concentration\n"
  "	cao = 2       (mM)       : initial external Ca++ concentration\n"
  "        tfa = 1                  : activation time constant scaling factor\n"
  "        tfi = 0.68               : inactivation time constant scaling factor\n"
  "        eca = 140                : Ca++ reversal potential\n"
  "}\n"
  "\n"
  "NEURON {\n"
  "	SUFFIX cat\n"
  "	USEION ca READ cai,cao \n"
  "        USEION Ca WRITE iCa VALENCE 2\n"
  "        : The T-current does not activate calcium-dependent currents.\n"
  "        : The construction with dummy ion Ca prevents the updating of the \n"
  "        : internal calcium concentration. \n"
  "        RANGE gcatbar, hinf, minf, taum, tauh, iCa\n"
  "}\n"
  "\n"
  "STATE {	m h }  : unknown activation and inactivation parameters to be solved in the DEs \n"
  "\n"
  "ASSIGNED {     : parameters needed to solve DE\n"
  "	iCa (mA/cm2)\n"
  "        gcat  (mho/cm2) \n"
  "        minf\n"
  "        hinf\n"
  "        taum\n"
  "        tauh\n"
  "}\n"
  "\n"
  "INITIAL {\n"
  ":        tadj = 3^((celsius-tBase)/10)   : assume Q10 of 3\n"
  "	rates(v)\n"
  "        m = minf\n"
  "        h = hinf\n"
  "	gcat = gcatbar*m*m*h*h2(cai)\n"
  "}\n"
  "\n"
  "BREAKPOINT {\n"
  "	SOLVE states\n"
  "	gcat = gcatbar*m*m*h*h2(cai) : maximum channel permeability\n"
  "	iCa = gcat*ghk(v,cai,cao)    : dummy calcium current induced by this channel\n"
  "\n"
  "}\n"
  "\n"
  "UNITSOFF\n"
  "FUNCTION h2(cai(mM)) {\n"
  "	h2 = ki/(ki+cai)\n"
  "}\n"
  "\n"
  "FUNCTION ghk(v(mV), ci(mM), co(mM)) (mV) { LOCAL nu,f\n"
  "        f = KTF(celsius)/2\n"
  "        nu = v/f\n"
  "        ghk=-f*(1. - (ci/co)*exp(nu))*efun(nu)\n"
  "}\n"
  "\n"
  "FUNCTION KTF(celsius (degC)) (mV) {   : temperature-dependent adjustment factor\n"
  "        KTF = ((25./293.15)*(celsius + 273.15))\n"
  "}\n"
  "\n"
  "FUNCTION efun(z) {\n"
  "	if (fabs(z) < 1e-4) {\n"
  "		efun = 1 - z/2\n"
  "	}else{\n"
  "		efun = z/(exp(z) - 1)\n"
  "	}\n"
  "}\n"
  "\n"
  "FUNCTION alph(v(mV)) {\n"
  "	TABLE FROM -150 TO 150 WITH 200\n"
  "	alph = 1.6e-4*exp(-(v+57)/19)\n"
  "}\n"
  "\n"
  "FUNCTION beth(v(mV)) {\n"
  "        TABLE FROM -150 TO 150 WITH 200\n"
  "	beth = 1/(exp((-v+15)/10)+1.0)\n"
  "}\n"
  "\n"
  "FUNCTION alpm(v(mV)) {\n"
  "	TABLE FROM -150 TO 150 WITH 200\n"
  "	alpm = 0.1967*(-1.0*v+19.88)/(exp((-1.0*v+19.88)/10.0)-1.0)\n"
  "}\n"
  "\n"
  "FUNCTION betm(v(mV)) {\n"
  "	TABLE FROM -150 TO 150 WITH 200\n"
  "	betm = 0.046*exp(-v/22.73)\n"
  "}\n"
  "\n"
  "UNITSON\n"
  "LOCAL facm,fach\n"
  "\n"
  ":if state_cagk is called from hoc, garbage or segmentation violation will\n"
  ":result because range variables won't have correct pointer.  This is because\n"
  ": only BREAKPOINT sets up the correct pointers to range variables.\n"
  "PROCEDURE states() {     : exact when v held constant; integrates over dt step\n"
  "        rates(v)\n"
  "        m = m + facm*(minf - m)\n"
  "        h = h + fach*(hinf - h)\n"
  "        VERBATIM\n"
  "        return 0;\n"
  "        ENDVERBATIM\n"
  "}\n"
  "\n"
  "PROCEDURE rates(v (mV)) { :callable from hoc\n"
  "        LOCAL a\n"
  "        a = alpm(v)\n"
  "        taum = 1/(tfa*(a + betm(v))) : estimation of activation tau\n"
  "        minf =  a/(a+betm(v))        : estimation of activation steady state\n"
  "        facm = (1 - exp(-dt/taum))\n"
  "        a = alph(v)\n"
  "        tauh = 1/(tfi*(a + beth(v))) : estimation of inactivation tau\n"
  "        hinf = a/(a+beth(v))         : estimation of inactivation steady state\n"
  "        fach = (1 - exp(-dt/tauh))\n"
  "}\n"
  ;
    hoc_reg_nmodl_filename(mech_type, nmodl_filename);
    hoc_reg_nmodl_text(mech_type, nmodl_file_text);
}
#endif
