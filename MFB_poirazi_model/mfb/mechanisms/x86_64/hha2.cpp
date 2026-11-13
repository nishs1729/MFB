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
static constexpr auto number_of_datum_variables = 6;
static constexpr auto number_of_floating_point_variables = 23;
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
 
#define nrn_init _nrn_init__hha2
#define _nrn_initial _nrn_initial__hha2
#define nrn_cur _nrn_cur__hha2
#define _nrn_current _nrn_current__hha2
#define nrn_jacob _nrn_jacob__hha2
#define nrn_state _nrn_state__hha2
#define _net_receive _net_receive__hha2 
#define calcg calcg__hha2 
#define mhn mhn__hha2 
#define states states__hha2 
 
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
#define ar2 _ml->template fpfield<0>(_iml)
#define ar2_columnindex 0
#define W _ml->template fpfield<1>(_iml)
#define W_columnindex 1
#define gnabar _ml->template fpfield<2>(_iml)
#define gnabar_columnindex 2
#define gkbar _ml->template fpfield<3>(_iml)
#define gkbar_columnindex 3
#define gl _ml->template fpfield<4>(_iml)
#define gl_columnindex 4
#define el _ml->template fpfield<5>(_iml)
#define el_columnindex 5
#define il _ml->template fpfield<6>(_iml)
#define il_columnindex 6
#define inf _ml->template data_array<7, 4>(_iml)
#define inf_columnindex 7
#define fac _ml->template data_array<8, 4>(_iml)
#define fac_columnindex 8
#define tau _ml->template data_array<9, 4>(_iml)
#define tau_columnindex 9
#define m _ml->template fpfield<10>(_iml)
#define m_columnindex 10
#define h _ml->template fpfield<11>(_iml)
#define h_columnindex 11
#define n _ml->template fpfield<12>(_iml)
#define n_columnindex 12
#define s _ml->template fpfield<13>(_iml)
#define s_columnindex 13
#define ena _ml->template fpfield<14>(_iml)
#define ena_columnindex 14
#define ek _ml->template fpfield<15>(_iml)
#define ek_columnindex 15
#define Dm _ml->template fpfield<16>(_iml)
#define Dm_columnindex 16
#define Dh _ml->template fpfield<17>(_iml)
#define Dh_columnindex 17
#define Dn _ml->template fpfield<18>(_iml)
#define Dn_columnindex 18
#define Ds _ml->template fpfield<19>(_iml)
#define Ds_columnindex 19
#define ina _ml->template fpfield<20>(_iml)
#define ina_columnindex 20
#define ik _ml->template fpfield<21>(_iml)
#define ik_columnindex 21
#define _g _ml->template fpfield<22>(_iml)
#define _g_columnindex 22
#define _ion_ena *(_ml->dptr_field<0>(_iml))
#define _p_ion_ena static_cast<neuron::container::data_handle<double>>(_ppvar[0])
#define _ion_ina *(_ml->dptr_field<1>(_iml))
#define _p_ion_ina static_cast<neuron::container::data_handle<double>>(_ppvar[1])
#define _ion_dinadv *(_ml->dptr_field<2>(_iml))
#define _ion_ek *(_ml->dptr_field<3>(_iml))
#define _p_ion_ek static_cast<neuron::container::data_handle<double>>(_ppvar[3])
#define _ion_ik *(_ml->dptr_field<4>(_iml))
#define _p_ion_ik static_cast<neuron::container::data_handle<double>>(_ppvar[4])
#define _ion_dikdv *(_ml->dptr_field<5>(_iml))
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
 static void _hoc_alpr(void);
 static void _hoc_alpv(void);
 static void _hoc_betr(void);
 static void _hoc_calcg(void);
 static void _hoc_mhn(void);
 static void _hoc_states(void);
 static void _hoc_vartau(void);
 static void _hoc_varss(void);
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
 {"setdata_hha2", _hoc_setdata},
 {"alpr_hha2", _hoc_alpr},
 {"alpv_hha2", _hoc_alpv},
 {"betr_hha2", _hoc_betr},
 {"calcg_hha2", _hoc_calcg},
 {"mhn_hha2", _hoc_mhn},
 {"states_hha2", _hoc_states},
 {"vartau_hha2", _hoc_vartau},
 {"varss_hha2", _hoc_varss},
 {0, 0}
};
 
/* Direct Python call wrappers to density mechanism functions.*/
 static double _npy_alpr(Prop*);
 static double _npy_alpv(Prop*);
 static double _npy_betr(Prop*);
 static double _npy_calcg(Prop*);
 static double _npy_mhn(Prop*);
 static double _npy_states(Prop*);
 static double _npy_vartau(Prop*);
 static double _npy_varss(Prop*);
 
static NPyDirectMechFunc npy_direct_func_proc[] = {
 {"alpr", _npy_alpr},
 {"alpv", _npy_alpv},
 {"betr", _npy_betr},
 {"calcg", _npy_calcg},
 {"mhn", _npy_mhn},
 {"states", _npy_states},
 {"vartau", _npy_vartau},
 {"varss", _npy_varss},
 {0, 0}
};
#define alpr alpr_hha2
#define alpv alpv_hha2
#define betr betr_hha2
#define vartau vartau_hha2
#define varss varss_hha2
 extern double alpr( double );
 extern double alpv( double , double );
 extern double betr( double );
 extern double vartau( double , double );
 extern double varss( double , double );
 /* declare global and static user variables */
 #define gind 0
 #define _gth 0
#define a0r a0r_hha2
 double a0r = 0.0003;
#define b0r b0r_hha2
 double b0r = 0.0003;
#define gmr gmr_hha2
 double gmr = 0.2;
#define taumin taumin_hha2
 double taumin = 3;
#define vhalfr vhalfr_hha2
 double vhalfr = -60;
#define vvs vvs_hha2
 double vvs = 2;
#define zetas zetas_hha2
 double zetas = 12;
#define zetar zetar_hha2
 double zetar = 12;
 /* some parameters have upper and lower limits */
 static HocParmLimits _hoc_parm_limits[] = {
 {0, 0, 0}
};
 static HocParmUnits _hoc_parm_units[] = {
 {"a0r_hha2", "ms"},
 {"b0r_hha2", "ms"},
 {"taumin_hha2", "ms"},
 {"vvs_hha2", "mV"},
 {"vhalfr_hha2", "mV"},
 {"W_hha2", "/mV"},
 {"gnabar_hha2", "mho/cm2"},
 {"gkbar_hha2", "mho/cm2"},
 {"gl_hha2", "mho/cm2"},
 {"el_hha2", "mV"},
 {"il_hha2", "mA/cm2"},
 {0, 0}
};
 static double delta_t = 0.01;
 static double h0 = 0;
 static double m0 = 0;
 static double n0 = 0;
 static double s0 = 0;
 static double v = 0;
 /* connect global user variables to hoc */
 static DoubScal hoc_scdoub[] = {
 {"a0r_hha2", &a0r_hha2},
 {"b0r_hha2", &b0r_hha2},
 {"zetar_hha2", &zetar_hha2},
 {"zetas_hha2", &zetas_hha2},
 {"gmr_hha2", &gmr_hha2},
 {"taumin_hha2", &taumin_hha2},
 {"vvs_hha2", &vvs_hha2},
 {"vhalfr_hha2", &vhalfr_hha2},
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
"hha2",
 "ar2_hha2",
 "W_hha2",
 "gnabar_hha2",
 "gkbar_hha2",
 "gl_hha2",
 "el_hha2",
 0,
 "il_hha2",
 "inf_hha2[4]",
 "fac_hha2[4]",
 "tau_hha2[4]",
 0,
 "m_hha2",
 "h_hha2",
 "n_hha2",
 "s_hha2",
 0,
 0};
 static Symbol* _na_sym;
 static Symbol* _k_sym;
 
 /* Used by NrnProperty */
 static _nrn_mechanism_std_vector<double> _parm_default{
     1, /* ar2 */
     0.016, /* W */
     0, /* gnabar */
     0, /* gkbar */
     0, /* gl */
     -70, /* el */
 }; 
 
 
extern Prop* need_memb(Symbol*);
static void nrn_alloc(Prop* _prop) {
  Prop *prop_ion{};
  Datum *_ppvar{};
   _ppvar = nrn_prop_datum_alloc(_mechtype, 6, _prop);
    _nrn_mechanism_access_dparam(_prop) = _ppvar;
     _nrn_mechanism_cache_instance _ml_real{_prop};
    auto* const _ml = &_ml_real;
    size_t const _iml{};
    assert(_nrn_mechanism_get_num_vars(_prop) == 23);
 	/*initialize range parameters*/
 	ar2 = _parm_default[0]; /* 1 */
 	W = _parm_default[1]; /* 0.016 */
 	gnabar = _parm_default[2]; /* 0 */
 	gkbar = _parm_default[3]; /* 0 */
 	gl = _parm_default[4]; /* 0 */
 	el = _parm_default[5]; /* -70 */
 	 assert(_nrn_mechanism_get_num_vars(_prop) == 23);
 	_nrn_mechanism_access_dparam(_prop) = _ppvar;
 	/*connect ionic variables to this model*/
 prop_ion = need_memb(_na_sym);
 nrn_promote(prop_ion, 0, 1);
 	_ppvar[0] = _nrn_mechanism_get_param_handle(prop_ion, 0); /* ena */
 	_ppvar[1] = _nrn_mechanism_get_param_handle(prop_ion, 3); /* ina */
 	_ppvar[2] = _nrn_mechanism_get_param_handle(prop_ion, 4); /* _ion_dinadv */
 prop_ion = need_memb(_k_sym);
 nrn_promote(prop_ion, 0, 1);
 	_ppvar[3] = _nrn_mechanism_get_param_handle(prop_ion, 0); /* ek */
 	_ppvar[4] = _nrn_mechanism_get_param_handle(prop_ion, 3); /* ik */
 	_ppvar[5] = _nrn_mechanism_get_param_handle(prop_ion, 4); /* _ion_dikdv */
 
}
 static void _initlists();
 extern Symbol* hoc_lookup(const char*);
extern void _nrn_thread_reg(int, int, void(*)(Datum*));
void _nrn_thread_table_reg(int, nrn_thread_table_check_t);
extern void hoc_register_tolerance(int, HocStateTolerance*, Symbol***);
extern void _cvode_abstol( Symbol**, double*, int);

 extern "C" void _hha2_reg() {
	int _vectorized = 0;
  _initlists();
 	ion_reg("na", -10000.);
 	ion_reg("k", -10000.);
 	_na_sym = hoc_lookup("na_ion");
 	_k_sym = hoc_lookup("k_ion");
 	register_mech(_mechanism, nrn_alloc,nrn_cur, nrn_jacob, nrn_state, nrn_init, hoc_nrnpointerindex, 0);
 _mechtype = nrn_get_mechtype(_mechanism[1]);
 hoc_register_parm_default(_mechtype, &_parm_default);
         hoc_register_npy_direct(_mechtype, npy_direct_func_proc);
     _nrn_setdata_reg(_mechtype, _setdata);
 #if NMODL_TEXT
  register_nmodl_text_and_filename(_mechtype);
#endif
   _nrn_mechanism_register_data_fields(_mechtype,
                                       _nrn_mechanism_field<double>{"ar2"} /* 0 */,
                                       _nrn_mechanism_field<double>{"W"} /* 1 */,
                                       _nrn_mechanism_field<double>{"gnabar"} /* 2 */,
                                       _nrn_mechanism_field<double>{"gkbar"} /* 3 */,
                                       _nrn_mechanism_field<double>{"gl"} /* 4 */,
                                       _nrn_mechanism_field<double>{"el"} /* 5 */,
                                       _nrn_mechanism_field<double>{"il"} /* 6 */,
                                       _nrn_mechanism_field<double>{"inf", 4} /* 7 */,
                                       _nrn_mechanism_field<double>{"fac", 4} /* 8 */,
                                       _nrn_mechanism_field<double>{"tau", 4} /* 9 */,
                                       _nrn_mechanism_field<double>{"m"} /* 10 */,
                                       _nrn_mechanism_field<double>{"h"} /* 11 */,
                                       _nrn_mechanism_field<double>{"n"} /* 12 */,
                                       _nrn_mechanism_field<double>{"s"} /* 13 */,
                                       _nrn_mechanism_field<double>{"ena"} /* 14 */,
                                       _nrn_mechanism_field<double>{"ek"} /* 15 */,
                                       _nrn_mechanism_field<double>{"Dm"} /* 16 */,
                                       _nrn_mechanism_field<double>{"Dh"} /* 17 */,
                                       _nrn_mechanism_field<double>{"Dn"} /* 18 */,
                                       _nrn_mechanism_field<double>{"Ds"} /* 19 */,
                                       _nrn_mechanism_field<double>{"ina"} /* 20 */,
                                       _nrn_mechanism_field<double>{"ik"} /* 21 */,
                                       _nrn_mechanism_field<double>{"_g"} /* 22 */,
                                       _nrn_mechanism_field<double*>{"_ion_ena", "na_ion"} /* 0 */,
                                       _nrn_mechanism_field<double*>{"_ion_ina", "na_ion"} /* 1 */,
                                       _nrn_mechanism_field<double*>{"_ion_dinadv", "na_ion"} /* 2 */,
                                       _nrn_mechanism_field<double*>{"_ion_ek", "k_ion"} /* 3 */,
                                       _nrn_mechanism_field<double*>{"_ion_ik", "k_ion"} /* 4 */,
                                       _nrn_mechanism_field<double*>{"_ion_dikdv", "k_ion"} /* 5 */);
  hoc_register_prop_size(_mechtype, 32, 6);
  hoc_register_dparam_semantics(_mechtype, 0, "na_ion");
  hoc_register_dparam_semantics(_mechtype, 1, "na_ion");
  hoc_register_dparam_semantics(_mechtype, 2, "na_ion");
  hoc_register_dparam_semantics(_mechtype, 3, "k_ion");
  hoc_register_dparam_semantics(_mechtype, 4, "k_ion");
  hoc_register_dparam_semantics(_mechtype, 5, "k_ion");
 	hoc_register_cvode(_mechtype, _ode_count, 0, 0, 0);
 
    hoc_register_var(hoc_scdoub, hoc_vdoub, hoc_intfunc);
 	ivoc_help("help ?1 hha2 /home/nishant/lab/project_MFB/MFB_poirazi_model/mfb/mechanisms/hha2.mod\n");
 hoc_register_limits(_mechtype, _hoc_parm_limits);
 hoc_register_units(_mechtype, _hoc_parm_units);
 }
static int _reset;
static const char *modelname = "HH channel that includes both a sodium and a delayed rectifier channel ";

static int error;
static int _ninits = 0;
static int _match_recurse=1;
static void _modl_cleanup(){ _match_recurse=1;}
static int calcg();
static int mhn(double);
static int states();
 
static int  calcg (  ) {
   mhn ( _threadargscomma_ v * 1.0 ) ;
   m = m + fac [ 0 ] * ( inf [ 0 ] - m ) ;
   h = h + fac [ 1 ] * ( inf [ 1 ] - h ) ;
   n = n + fac [ 2 ] * ( inf [ 2 ] - n ) ;
   s = s + fac [ 3 ] * ( inf [ 3 ] - s ) ;
    return 0; }
 
static void _hoc_calcg(void) {
  double _r;
  
  if(!_prop_id) {
    hoc_execerror("No data for calcg_hha2. Requires prior call to setdata_hha2 and that the specified mechanism instance still be in existence.", NULL);
  } else {
    _setdata(_extcall_prop);
  }
   _r = 1.;
 calcg (  );
 hoc_retpushx(_r);
}
 
static double _npy_calcg(Prop* _prop) {
    double _r{0.0};
    neuron::legacy::set_globals_from_prop(_prop, _ml_real, _ml, _iml);
  _ppvar = _nrn_mechanism_access_dparam(_prop);
 _r = 1.;
 calcg (  );
 return(_r);
}
 
static int  states (  ) {
   calcg ( _threadargs_ ) ;
   
/*VERBATIM*/
	return 0;
  return 0; }
 
static void _hoc_states(void) {
  double _r;
  
  if(!_prop_id) {
    hoc_execerror("No data for states_hha2. Requires prior call to setdata_hha2 and that the specified mechanism instance still be in existence.", NULL);
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
 
double varss (  double _lv , double _li ) {
   double _lvarss;
 if ( _li  == 0.0 ) {
     _lvarss = 1.0 / ( 1.0 + exp ( ( _lv + 44.0 ) / ( - 3.0 ) ) ) ;
     }
   else if ( _li  == 1.0 ) {
     _lvarss = 1.0 / ( 1.0 + exp ( ( _lv + 49.0 ) / ( 3.5 ) ) ) ;
     }
   else if ( _li  == 2.0 ) {
     _lvarss = 1.0 / ( 1.0 + exp ( ( _lv + 46.3 ) / ( - 3.0 ) ) ) ;
     }
   else {
     _lvarss = alpv ( _threadargscomma_ _lv , vhalfr ) ;
     }
   
return _lvarss;
 }
 
static void _hoc_varss(void) {
  double _r;
  
  if(!_prop_id) {
    hoc_execerror("No data for varss_hha2. Requires prior call to setdata_hha2 and that the specified mechanism instance still be in existence.", NULL);
  } else {
    _setdata(_extcall_prop);
  }
   _r =  varss (  *getarg(1) , *getarg(2) );
 hoc_retpushx(_r);
}
 
static double _npy_varss(Prop* _prop) {
    double _r{0.0};
    neuron::legacy::set_globals_from_prop(_prop, _ml_real, _ml, _iml);
  _ppvar = _nrn_mechanism_access_dparam(_prop);
 _r =  varss (  *getarg(1) , *getarg(2) );
 return(_r);
}
 
double alpv (  double _lv , double _lvh ) {
   double _lalpv;
 _lalpv = ( 1.0 + ar2 * exp ( ( _lv - _lvh ) / vvs ) ) / ( 1.0 + exp ( ( _lv - _lvh ) / vvs ) ) ;
   
return _lalpv;
 }
 
static void _hoc_alpv(void) {
  double _r;
  
  if(!_prop_id) {
    hoc_execerror("No data for alpv_hha2. Requires prior call to setdata_hha2 and that the specified mechanism instance still be in existence.", NULL);
  } else {
    _setdata(_extcall_prop);
  }
   _r =  alpv (  *getarg(1) , *getarg(2) );
 hoc_retpushx(_r);
}
 
static double _npy_alpv(Prop* _prop) {
    double _r{0.0};
    neuron::legacy::set_globals_from_prop(_prop, _ml_real, _ml, _iml);
  _ppvar = _nrn_mechanism_access_dparam(_prop);
 _r =  alpv (  *getarg(1) , *getarg(2) );
 return(_r);
}
 
double alpr (  double _lv ) {
   double _lalpr;
 _lalpr = exp ( 1.e-3 * zetar * ( _lv - vhalfr ) * 9.648e4 / ( 8.315 * ( 273.16 + celsius ) ) ) ;
   
return _lalpr;
 }
 
static void _hoc_alpr(void) {
  double _r;
    _r =  alpr (  *getarg(1) );
 hoc_retpushx(_r);
}
 
static double _npy_alpr(Prop* _prop) {
    double _r{0.0};
    neuron::legacy::set_globals_from_prop(_prop, _ml_real, _ml, _iml);
  _ppvar = _nrn_mechanism_access_dparam(_prop);
 _r =  alpr (  *getarg(1) );
 return(_r);
}
 
double betr (  double _lv ) {
   double _lbetr;
 _lbetr = exp ( 1.e-3 * zetar * gmr * ( _lv - vhalfr ) * 9.648e4 / ( 8.315 * ( 273.16 + celsius ) ) ) ;
   
return _lbetr;
 }
 
static void _hoc_betr(void) {
  double _r;
    _r =  betr (  *getarg(1) );
 hoc_retpushx(_r);
}
 
static double _npy_betr(Prop* _prop) {
    double _r{0.0};
    neuron::legacy::set_globals_from_prop(_prop, _ml_real, _ml, _iml);
  _ppvar = _nrn_mechanism_access_dparam(_prop);
 _r =  betr (  *getarg(1) );
 return(_r);
}
 
double vartau (  double _lv , double _li ) {
   double _lvartau;
 double _ltmp ;
 if ( _li  == 0.0 ) {
     _lvartau = 0.05 ;
     }
   else if ( _li  == 1.0 ) {
     _lvartau = 1.0 ;
     }
   else if ( _li  == 2.0 ) {
     _lvartau = 3.5 ;
     }
   else {
     _ltmp = betr ( _threadargscomma_ _lv ) / ( a0r + b0r * alpr ( _threadargscomma_ _lv ) ) ;
     if ( _ltmp < taumin ) {
       _ltmp = taumin ;
       }
     
/*VERBATIM*/
 _lvartau = _ltmp ;
     }
   
return _lvartau;
 }
 
static void _hoc_vartau(void) {
  double _r;
  
  if(!_prop_id) {
    hoc_execerror("No data for vartau_hha2. Requires prior call to setdata_hha2 and that the specified mechanism instance still be in existence.", NULL);
  } else {
    _setdata(_extcall_prop);
  }
   _r =  vartau (  *getarg(1) , *getarg(2) );
 hoc_retpushx(_r);
}
 
static double _npy_vartau(Prop* _prop) {
    double _r{0.0};
    neuron::legacy::set_globals_from_prop(_prop, _ml_real, _ml, _iml);
  _ppvar = _nrn_mechanism_access_dparam(_prop);
 _r =  vartau (  *getarg(1) , *getarg(2) );
 return(_r);
}
 
static int  mhn (  double _lv ) {
   double _la , _lb ;
 {int  _li ;for ( _li = 0 ; _li <= 3 ; _li ++ ) {
     tau [ _li ] = vartau ( _threadargscomma_ _lv , ((double) _li ) ) ;
     inf [ _li ] = varss ( _threadargscomma_ _lv , ((double) _li ) ) ;
     fac [ _li ] = ( 1.0 - exp ( - dt / tau [ _li ] ) ) ;
     } }
    return 0; }
 
static void _hoc_mhn(void) {
  double _r;
  
  if(!_prop_id) {
    hoc_execerror("No data for mhn_hha2. Requires prior call to setdata_hha2 and that the specified mechanism instance still be in existence.", NULL);
  } else {
    _setdata(_extcall_prop);
  }
   _r = 1.;
 mhn (  *getarg(1) );
 hoc_retpushx(_r);
}
 
static double _npy_mhn(Prop* _prop) {
    double _r{0.0};
    neuron::legacy::set_globals_from_prop(_prop, _ml_real, _ml, _iml);
  _ppvar = _nrn_mechanism_access_dparam(_prop);
 _r = 1.;
 mhn (  *getarg(1) );
 return(_r);
}
 
static int _ode_count(int _type){ hoc_execerror("hha2", "cannot be used with CVODE"); return 0;}

static void initmodel() {
  int _i; double _save;_ninits++;
 _save = t;
 t = 0.0;
{
  h = h0;
  m = m0;
  n = n0;
  s = s0;
 {
   states ( _threadargs_ ) ;
   s = 1.0 ;
   ina = gnabar * m * m * h * s * ( v - ena ) ;
   ik = gkbar * n * n * ( v - ek ) ;
   il = gl * ( v - el ) ;
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
  ena = _ion_ena;
  ek = _ion_ek;
 initmodel();
  }}

static double _nrn_current(double _v){double _current=0.;v=_v;{ {
   ina = gnabar * m * m * h * s * ( v - ena ) ;
   ik = gkbar * n * n * ( v - ek ) ;
   il = gl * ( v - el ) ;
   }
 _current += ina;
 _current += ik;
 _current += il;

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
  ena = _ion_ena;
  ek = _ion_ek;
 auto const _g_local = _nrn_current(_v + .001);
 	{ double _dik;
 double _dina;
  _dina = ina;
  _dik = ik;
 _rhs = _nrn_current(_v);
  _ion_dinadv += (_dina - ina)/.001 ;
  _ion_dikdv += (_dik - ik)/.001 ;
 	}
 _g = (_g_local - _rhs)/.001;
  _ion_ina += ina ;
  _ion_ik += ik ;
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
  ena = _ion_ena;
  ek = _ion_ek;
 { error =  states();
 if(error){
  std_cerr_stream << "at line 71 in file hha2.mod:\n	SOLVE states\n";
  std_cerr_stream << _ml << ' ' << _iml << '\n';
  abort_run(error);
}
 }  }}

}

static void terminal(){}

static void _initlists() {
 int _i; static int _first = 1;
  if (!_first) return;
_first = 0;
}

#if NMODL_TEXT
static void register_nmodl_text_and_filename(int mech_type) {
    const char* nmodl_filename = "/home/nishant/lab/project_MFB/MFB_poirazi_model/mfb/mechanisms/hha2.mod";
    const char* nmodl_file_text = 
  "TITLE HH channel that includes both a sodium and a delayed rectifier channel \n"
  ": and accounts for sodium conductance attenuation\n"
  ": Bartlett Mel-modified Hodgkin - Huxley conductances (after Ojvind et al.)\n"
  ": Terrence Brannon-added attenuation \n"
  ": Yiota Poirazi-modified Kdr and Na threshold and time constants to make it more stable\n"
  ": Yiota Poirazi-modified threshold for soma/axon spike initiation (threshold about -57 mV),\n"
  ": USC Los Angeles 2000, poirazi@LNC.usc.edu\n"
  ": This file is used only in soma and axon sections\n"
  "\n"
  "\n"
  "NEURON {\n"
  "	SUFFIX hha2\n"
  "	USEION na READ ena WRITE ina\n"
  "	USEION k READ ek WRITE ik\n"
  "	NONSPECIFIC_CURRENT il\n"
  "	RANGE gnabar, gkbar, gl, el\n"
  "	RANGE ar2, vhalfs\n"
  "	RANGE inf, fac, tau\n"
  "	RANGE taus\n"
  "	RANGE W\n"
  "	GLOBAL taumin\n"
  "}\n"
  "\n"
  "UNITS {\n"
  "	(mA) = (milliamp)\n"
  "	(mV) = (millivolt)\n"
  "}\n"
  "\n"
  "INDEPENDENT {t FROM 0 TO 1 WITH 1 (ms)}\n"
  "\n"
  "PARAMETER {                     :parameters that can be entered when function is called in cell-setup\n"
  " a0r = 0.0003 (ms)\n"
  "        b0r = 0.0003 (ms)\n"
  "        zetar = 12    \n"
  "	zetas = 12   \n"
  "        gmr = 0.2   \n"
  "	ar2 = 1.0               :initialized parameter for location-dependent\n"
  "                                :Na-conductance attenuation, \"s\", (ar=1 -> zero attenuation)\n"
  "	taumin = 3   (ms)       :min activation time for \"s\" attenuation system\n"
  "        vvs  = 2     (mV)       :slope for \"s\" attenuation system\n"
  "        vhalfr = -60 (mV)       :half potential for \"s\" attenuation system\n"
  "	W = 0.016    (/mV)      :this 1/61.5 mV\n"
  ":	gnabar = 0.2 (mho/cm2)  :suggested conductance values\n"
  ":	gkbar = 0.12 (mho/cm2)\n"
  ":	gl = 0.0001  (mho/cm2)\n"
  "        gnabar = 0   (mho/cm2)  :initialized conductances\n"
  "	gkbar = 0    (mho/cm2)  :actual values set in cell-setup.hoc\n"
  "	gl = 0       (mho/cm2)\n"
  "	ena = 60     (mV)       :Na reversal potential (also reset in\n"
  "	ek = -77     (mV)       :K reversal potential  cell-setup.hoc)\n"
  "	el = -70.0   (mV)       :steady state \n"
  "	celsius = 34 (degC)\n"
  "	v            (mV)\n"
  "        dt\n"
  "}\n"
  "\n"
  "STATE {				:the unknown parameters to be solved in the DEs\n"
  "	m h n s\n"
  "}\n"
  "\n"
  "ASSIGNED {			:parameters needed to solve DE\n"
  "	ina (mA/cm2)\n"
  "	ik (mA/cm2)\n"
  "	il (mA/cm2)\n"
  "	inf[4]\n"
  "	fac[4]\n"
  "	tau[4]\n"
  "}\n"
  "\n"
  "BREAKPOINT {\n"
  "	SOLVE states\n"
  "	ina = gnabar*m*m*h*s*(v - ena) :Sodium current\n"
  "	ik = gkbar*n*n*(v - ek)        :Potassium current\n"
  "	il = gl*(v - el)               :leak current\n"
  "}\n"
  "\n"
  "INITIAL {			:initialize the following parameter using states()\n"
  "	states()\n"
  "	s=1\n"
  "	ina = gnabar*m*m*h*s*(v - ena)\n"
  "	ik = gkbar*n*n*(v - ek)\n"
  "	il = gl*(v - el)\n"
  "}\n"
  "\n"
  "PROCEDURE calcg() {\n"
  "	mhn(v*1(/mV))\n"
  "	m = m + fac[0]*(inf[0] - m)  :Na activation variable\n"
  "	h = h + fac[1]*(inf[1] - h)  :Na inactivation variable\n"
  "	n = n + fac[2]*(inf[2] - n)  :K activation variable\n"
  "	s = s + fac[3]*(inf[3] - s)  :Na attenuation variable\n"
  "}	\n"
  "\n"
  "PROCEDURE states() {	: exact when v held constant\n"
  "	calcg()\n"
  "	VERBATIM\n"
  "	return 0;\n"
  "	ENDVERBATIM\n"
  "}\n"
  "\n"
  "FUNCTION varss(v, i) { :steady state values\n"
  "	if (i==0) {\n"
  "                varss = 1 / (1 + exp((v + 44)/(-3)))    :Na activation\n"
  " 	}\n"
  "	else if (i==1) {\n"
  "                varss = 1 / (1 + exp((v + 49)/(3.5)))   :Na inactivation \n"
  "	}\n"
  "	else if (i==2) {	\n"
  "                varss = 1 / (1 + exp((v + 46.3)/(-3))) :K activation\n"
  "\n"
  "	} else {\n"
  "                :\"s\" activation system for spike attenuation - Migliore 96 model\n"
  "		varss =     alpv(v,vhalfr)\n"
  "       }\n"
  "}\n"
  "\n"
  "FUNCTION alpv(v(mV),vh) {    :used in \"s\" activation system infinity calculation\n"
  "  alpv = (1+ar2*exp((v-vh)/vvs))/(1+exp((v-vh)/vvs))\n"
  "}\n"
  "\n"
  "FUNCTION alpr(v(mV)) {       :used in \"s\" activation system tau\n"
  "  alpr = exp(1.e-3*zetar*(v-vhalfr)*9.648e4/(8.315*(273.16+celsius))) \n"
  "}\n"
  "\n"
  "FUNCTION betr(v(mV)) {       :used in \"s\" activation system tau\n"
  "  betr = exp(1.e-3*zetar*gmr*(v-vhalfr)*9.648e4/(8.315*(273.16+celsius))) \n"
  "}\n"
  "\n"
  "FUNCTION vartau(v, i) { :estimate tau values\n"
  "	LOCAL tmp\n"
  "\n"
  "	if (i==0) {\n"
  "	    vartau = 0.05  :Na activation tau\n"
  "	}\n"
  "	else if (i==1) {\n"
  "            vartau = 1     :Na inactivation tau\n"
  "	}\n"
  "	else if (i==2) {\n"
  "            vartau = 3.5   :K activation\n"
  "       	} else {\n"
  "	     tmp = betr(v)/(a0r+b0r*alpr(v))\n"
  "	     if (tmp<taumin) {tmp=taumin}\n"
  "	VERBATIM\n"
  "	ENDVERBATIM\n"
  "	     vartau = tmp   :s activation tau\n"
  "       }\n"
  "}	\n"
  "\n"
  "PROCEDURE mhn(v) {LOCAL a, b :rest = -70\n"
  ":       TABLE infinity, tau, fac DEPEND dt, celsius FROM -100 TO 100 WITH 200\n"
  "	FROM i=0 TO 3 {\n"
  "		tau[i] = vartau(v,i)\n"
  "		inf[i] = varss(v,i)\n"
  "		fac[i] = (1 - exp(-dt/tau[i]))\n"
  "	}\n"
  "}\n"
  "\n"
  "\n"
  "\n"
  "\n"
  "\n"
  "\n"
  "\n"
  "\n"
  "\n"
  "\n"
  "\n"
  "\n"
  "\n"
  "\n"
  "\n"
  ;
    hoc_reg_nmodl_filename(mech_type, nmodl_filename);
    hoc_reg_nmodl_text(mech_type, nmodl_file_text);
}
#endif
