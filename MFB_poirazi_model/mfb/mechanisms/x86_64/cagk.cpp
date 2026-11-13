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
static constexpr auto number_of_datum_variables = 5;
static constexpr auto number_of_floating_point_variables = 7;
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
 
#define nrn_init _nrn_init__mykca
#define _nrn_initial _nrn_initial__mykca
#define nrn_cur _nrn_cur__mykca
#define _nrn_current _nrn_current__mykca
#define nrn_jacob _nrn_jacob__mykca
#define nrn_state _nrn_state__mykca
#define _net_receive _net_receive__mykca 
#define rate rate__mykca 
#define state state__mykca 
 
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
#define gkbar _ml->template fpfield<0>(_iml)
#define gkbar_columnindex 0
#define ik _ml->template fpfield<1>(_iml)
#define ik_columnindex 1
#define o _ml->template fpfield<2>(_iml)
#define o_columnindex 2
#define ek _ml->template fpfield<3>(_iml)
#define ek_columnindex 3
#define cai _ml->template fpfield<4>(_iml)
#define cai_columnindex 4
#define Do _ml->template fpfield<5>(_iml)
#define Do_columnindex 5
#define _g _ml->template fpfield<6>(_iml)
#define _g_columnindex 6
#define _ion_cai *(_ml->dptr_field<0>(_iml))
#define _p_ion_cai static_cast<neuron::container::data_handle<double>>(_ppvar[0])
#define _ion_cao *(_ml->dptr_field<1>(_iml))
#define _p_ion_cao static_cast<neuron::container::data_handle<double>>(_ppvar[1])
#define _ion_ek *(_ml->dptr_field<2>(_iml))
#define _p_ion_ek static_cast<neuron::container::data_handle<double>>(_ppvar[2])
#define _ion_ik *(_ml->dptr_field<3>(_iml))
#define _p_ion_ik static_cast<neuron::container::data_handle<double>>(_ppvar[3])
#define _ion_dikdv *(_ml->dptr_field<4>(_iml))
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
 static void _hoc_alp(void);
 static void _hoc_bet(void);
 static void _hoc_exp1(void);
 static void _hoc_rate(void);
 static void _hoc_state(void);
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
 {"setdata_mykca", _hoc_setdata},
 {"alp_mykca", _hoc_alp},
 {"bet_mykca", _hoc_bet},
 {"exp1_mykca", _hoc_exp1},
 {"rate_mykca", _hoc_rate},
 {"state_mykca", _hoc_state},
 {0, 0}
};
 
/* Direct Python call wrappers to density mechanism functions.*/
 static double _npy_alp(Prop*);
 static double _npy_bet(Prop*);
 static double _npy_exp1(Prop*);
 static double _npy_rate(Prop*);
 static double _npy_state(Prop*);
 
static NPyDirectMechFunc npy_direct_func_proc[] = {
 {"alp", _npy_alp},
 {"bet", _npy_bet},
 {"exp1", _npy_exp1},
 {"rate", _npy_rate},
 {"state", _npy_state},
 {0, 0}
};
#define alp alp_mykca
#define bet bet_mykca
#define exp1 exp1_mykca
 extern double alp( double , double );
 extern double bet( double , double );
 extern double exp1( double , double , double );
 /* declare global and static user variables */
 #define gind 0
 #define _gth 0
#define abar abar_mykca
 double abar = 0.48;
#define bbar bbar_mykca
 double bbar = 0.28;
#define d2 d2_mykca
 double d2 = 1;
#define d1 d1_mykca
 double d1 = 0.84;
#define k2 k2_mykca
 double k2 = 0.011;
#define k1 k1_mykca
 double k1 = 0.18;
#define oinf oinf_mykca
 double oinf = 0;
#define tau tau_mykca
 double tau = 0;
 /* some parameters have upper and lower limits */
 static HocParmLimits _hoc_parm_limits[] = {
 {0, 0, 0}
};
 static HocParmUnits _hoc_parm_units[] = {
 {"k1_mykca", "mM"},
 {"k2_mykca", "mM"},
 {"bbar_mykca", "/ms"},
 {"abar_mykca", "/ms"},
 {"tau_mykca", "ms"},
 {"gkbar_mykca", "mho/cm2"},
 {"ik_mykca", "mA/cm2"},
 {0, 0}
};
 static double delta_t = 0.01;
 static double o0 = 0;
 static double v = 0;
 /* connect global user variables to hoc */
 static DoubScal hoc_scdoub[] = {
 {"d1_mykca", &d1_mykca},
 {"d2_mykca", &d2_mykca},
 {"k1_mykca", &k1_mykca},
 {"k2_mykca", &k2_mykca},
 {"bbar_mykca", &bbar_mykca},
 {"abar_mykca", &abar_mykca},
 {"oinf_mykca", &oinf_mykca},
 {"tau_mykca", &tau_mykca},
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
"mykca",
 "gkbar_mykca",
 0,
 "ik_mykca",
 0,
 "o_mykca",
 0,
 0};
 static Symbol* _ca_sym;
 static Symbol* _k_sym;
 
 /* Used by NrnProperty */
 static _nrn_mechanism_std_vector<double> _parm_default{
     0.01, /* gkbar */
 }; 
 
 
extern Prop* need_memb(Symbol*);
static void nrn_alloc(Prop* _prop) {
  Prop *prop_ion{};
  Datum *_ppvar{};
   _ppvar = nrn_prop_datum_alloc(_mechtype, 5, _prop);
    _nrn_mechanism_access_dparam(_prop) = _ppvar;
     _nrn_mechanism_cache_instance _ml_real{_prop};
    auto* const _ml = &_ml_real;
    size_t const _iml{};
    assert(_nrn_mechanism_get_num_vars(_prop) == 7);
 	/*initialize range parameters*/
 	gkbar = _parm_default[0]; /* 0.01 */
 	 assert(_nrn_mechanism_get_num_vars(_prop) == 7);
 	_nrn_mechanism_access_dparam(_prop) = _ppvar;
 	/*connect ionic variables to this model*/
 prop_ion = need_memb(_ca_sym);
 nrn_promote(prop_ion, 1, 0);
 	_ppvar[0] = _nrn_mechanism_get_param_handle(prop_ion, 1); /* cai */
 	_ppvar[1] = _nrn_mechanism_get_param_handle(prop_ion, 2); /* cao */
 prop_ion = need_memb(_k_sym);
 nrn_promote(prop_ion, 0, 1);
 	_ppvar[2] = _nrn_mechanism_get_param_handle(prop_ion, 0); /* ek */
 	_ppvar[3] = _nrn_mechanism_get_param_handle(prop_ion, 3); /* ik */
 	_ppvar[4] = _nrn_mechanism_get_param_handle(prop_ion, 4); /* _ion_dikdv */
 
}
 static void _initlists();
 extern Symbol* hoc_lookup(const char*);
extern void _nrn_thread_reg(int, int, void(*)(Datum*));
void _nrn_thread_table_reg(int, nrn_thread_table_check_t);
extern void hoc_register_tolerance(int, HocStateTolerance*, Symbol***);
extern void _cvode_abstol( Symbol**, double*, int);

 extern "C" void _cagk_reg() {
	int _vectorized = 0;
  _initlists();
 	ion_reg("ca", -10000.);
 	ion_reg("k", -10000.);
 	_ca_sym = hoc_lookup("ca_ion");
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
                                       _nrn_mechanism_field<double>{"gkbar"} /* 0 */,
                                       _nrn_mechanism_field<double>{"ik"} /* 1 */,
                                       _nrn_mechanism_field<double>{"o"} /* 2 */,
                                       _nrn_mechanism_field<double>{"ek"} /* 3 */,
                                       _nrn_mechanism_field<double>{"cai"} /* 4 */,
                                       _nrn_mechanism_field<double>{"Do"} /* 5 */,
                                       _nrn_mechanism_field<double>{"_g"} /* 6 */,
                                       _nrn_mechanism_field<double*>{"_ion_cai", "ca_ion"} /* 0 */,
                                       _nrn_mechanism_field<double*>{"_ion_cao", "ca_ion"} /* 1 */,
                                       _nrn_mechanism_field<double*>{"_ion_ek", "k_ion"} /* 2 */,
                                       _nrn_mechanism_field<double*>{"_ion_ik", "k_ion"} /* 3 */,
                                       _nrn_mechanism_field<double*>{"_ion_dikdv", "k_ion"} /* 4 */);
  hoc_register_prop_size(_mechtype, 7, 5);
  hoc_register_dparam_semantics(_mechtype, 0, "ca_ion");
  hoc_register_dparam_semantics(_mechtype, 1, "ca_ion");
  hoc_register_dparam_semantics(_mechtype, 2, "k_ion");
  hoc_register_dparam_semantics(_mechtype, 3, "k_ion");
  hoc_register_dparam_semantics(_mechtype, 4, "k_ion");
 	hoc_register_cvode(_mechtype, _ode_count, 0, 0, 0);
 
    hoc_register_var(hoc_scdoub, hoc_vdoub, hoc_intfunc);
 	ivoc_help("help ?1 mykca /home/nishant/lab/project_MFB/MFB_poirazi_model/mfb/mechanisms/cagk.mod\n");
 hoc_register_limits(_mechtype, _hoc_parm_limits);
 hoc_register_units(_mechtype, _hoc_parm_units);
 }
 static double FARADAY = 0x1.81f0fae775425p+6;
 static double R = 8.313424;
 static double _zfac ;
static int _reset;
static const char *modelname = "CaGk";

static int error;
static int _ninits = 0;
static int _match_recurse=1;
static void _modl_cleanup(){ _match_recurse=1;}
static int rate(double, double);
static int state();
 
static int  state (  ) {
   rate ( _threadargscomma_ v , cai ) ;
   o = o + _zfac * ( oinf - o ) ;
   
/*VERBATIM*/
	return 0;
  return 0; }
 
static void _hoc_state(void) {
  double _r;
  
  if(!_prop_id) {
    hoc_execerror("No data for state_mykca. Requires prior call to setdata_mykca and that the specified mechanism instance still be in existence.", NULL);
  } else {
    _setdata(_extcall_prop);
  }
   _r = 1.;
 state (  );
 hoc_retpushx(_r);
}
 
static double _npy_state(Prop* _prop) {
    double _r{0.0};
    neuron::legacy::set_globals_from_prop(_prop, _ml_real, _ml, _iml);
  _ppvar = _nrn_mechanism_access_dparam(_prop);
 _r = 1.;
 state (  );
 return(_r);
}
 
double alp (  double _lv , double _lca ) {
   double _lalp;
 _lalp = abar / ( 1.0 + exp1 ( _threadargscomma_ k1 , d1 , _lv ) / _lca ) ;
   
return _lalp;
 }
 
static void _hoc_alp(void) {
  double _r;
    _r =  alp (  *getarg(1) , *getarg(2) );
 hoc_retpushx(_r);
}
 
static double _npy_alp(Prop* _prop) {
    double _r{0.0};
    neuron::legacy::set_globals_from_prop(_prop, _ml_real, _ml, _iml);
  _ppvar = _nrn_mechanism_access_dparam(_prop);
 _r =  alp (  *getarg(1) , *getarg(2) );
 return(_r);
}
 
double bet (  double _lv , double _lca ) {
   double _lbet;
 _lbet = bbar / ( 1.0 + _lca / exp1 ( _threadargscomma_ k2 , d2 , _lv ) ) ;
   
return _lbet;
 }
 
static void _hoc_bet(void) {
  double _r;
    _r =  bet (  *getarg(1) , *getarg(2) );
 hoc_retpushx(_r);
}
 
static double _npy_bet(Prop* _prop) {
    double _r{0.0};
    neuron::legacy::set_globals_from_prop(_prop, _ml_real, _ml, _iml);
  _ppvar = _nrn_mechanism_access_dparam(_prop);
 _r =  bet (  *getarg(1) , *getarg(2) );
 return(_r);
}
 
double exp1 (  double _lk , double _ld , double _lv ) {
   double _lexp1;
 _lexp1 = _lk * exp ( - 2.0 * _ld * FARADAY * _lv / R / ( 273.15 + celsius ) ) ;
   
return _lexp1;
 }
 
static void _hoc_exp1(void) {
  double _r;
    _r =  exp1 (  *getarg(1) , *getarg(2) , *getarg(3) );
 hoc_retpushx(_r);
}
 
static double _npy_exp1(Prop* _prop) {
    double _r{0.0};
    neuron::legacy::set_globals_from_prop(_prop, _ml_real, _ml, _iml);
  _ppvar = _nrn_mechanism_access_dparam(_prop);
 _r =  exp1 (  *getarg(1) , *getarg(2) , *getarg(3) );
 return(_r);
}
 
static int  rate (  double _lv , double _lca ) {
   double _la ;
 _la = alp ( _threadargscomma_ _lv , _lca ) ;
   tau = 1.0 / ( _la + bet ( _threadargscomma_ _lv , _lca ) ) ;
   oinf = _la * tau ;
   _zfac = ( 1.0 - exp ( - dt / tau ) ) ;
    return 0; }
 
static void _hoc_rate(void) {
  double _r;
    _r = 1.;
 rate (  *getarg(1) , *getarg(2) );
 hoc_retpushx(_r);
}
 
static double _npy_rate(Prop* _prop) {
    double _r{0.0};
    neuron::legacy::set_globals_from_prop(_prop, _ml_real, _ml, _iml);
  _ppvar = _nrn_mechanism_access_dparam(_prop);
 _r = 1.;
 rate (  *getarg(1) , *getarg(2) );
 return(_r);
}
 
static int _ode_count(int _type){ hoc_execerror("mykca", "cannot be used with CVODE"); return 0;}

static void initmodel() {
  int _i; double _save;_ninits++;
 _save = t;
 t = 0.0;
{
  o = o0;
 {
   rate ( _threadargscomma_ v , cai ) ;
   o = oinf ;
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
  ek = _ion_ek;
 initmodel();
 }}

static double _nrn_current(double _v){double _current=0.;v=_v;{ {
   ik = gkbar * o * ( v - ek ) ;
   }
 _current += ik;

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
  ek = _ion_ek;
 auto const _g_local = _nrn_current(_v + .001);
 	{ double _dik;
  _dik = ik;
 _rhs = _nrn_current(_v);
  _ion_dikdv += (_dik - ik)/.001 ;
 	}
 _g = (_g_local - _rhs)/.001;
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
  cai = _ion_cai;
  ek = _ion_ek;
 { error =  state();
 if(error){
  std_cerr_stream << "at line 64 in file cagk.mod:\n	SOLVE state\n";
  std_cerr_stream << _ml << ' ' << _iml << '\n';
  abort_run(error);
}
 } }}

}

static void terminal(){}

static void _initlists() {
 int _i; static int _first = 1;
  if (!_first) return;
_first = 0;
}

#if NMODL_TEXT
static void register_nmodl_text_and_filename(int mech_type) {
    const char* nmodl_filename = "/home/nishant/lab/project_MFB/MFB_poirazi_model/mfb/mechanisms/cagk.mod";
    const char* nmodl_file_text = 
  "TITLE CaGk\n"
  ": Calcium activated mAHP K channel.\n"
  ": From Moczydlowski and Latorre (1983) J. Gen. Physiol. 82\n"
  "\n"
  "UNITS {\n"
  "	(molar) = (1/liter)\n"
  "}\n"
  "\n"
  "UNITS {\n"
  "	(mV) =	(millivolt)\n"
  "	(mA) =	(milliamp)\n"
  "	(mM) =	(millimolar)\n"
  "}\n"
  "\n"
  "INDEPENDENT {t FROM 0 TO 1 WITH 100 (ms)}\n"
  "\n"
  "NEURON {\n"
  "	SUFFIX mykca\n"
  "	USEION ca READ cai\n"
  "	USEION k READ ek WRITE ik\n"
  "	RANGE gkbar, ik\n"
  "	GLOBAL oinf, tau\n"
  "}\n"
  "\n"
  "UNITS {\n"
  "	FARADAY = (faraday)  (kilocoulombs)\n"
  "	R = 8.313424 (joule/degC)\n"
  "}\n"
  "\n"
  "PARAMETER {\n"
  "	v		(mV)\n"
  "	dt		(ms)\n"
  "	ek		(mV)\n"
  "	celsius = 20	(degC)\n"
  "	gkbar = 0.01	(mho/cm2)	: Maximum Permeability\n"
  "	cai = 1e-3	(mM)\n"
  "	d1 = 0.84\n"
  "	d2 = 1.0\n"
  "	k1 = 0.18	(mM)\n"
  "	k2 = 0.011	(mM)\n"
  "	bbar = 0.28	(/ms)\n"
  "	abar = 0.48	(/ms)\n"
  "}\n"
  "COMMENT\n"
  "the preceding two numbers were switched on 8/19/92 in response to a bug\n"
  "report by Bartlett Mel. In the paper the kinetic scheme is\n"
  "C <-> CCa (K1)\n"
  "CCa <-> OCa (beta2,alpha2)\n"
  "OCa <-> OCa2 (K4)\n"
  "In this model abar = beta2 and bbar = alpha2 and K4 comes from d2 and k2\n"
  "I was forcing things into a nomenclature where alpha is the rate from\n"
  "closed to open. Unfortunately I didn't switch the numbers.\n"
  "ENDCOMMENT\n"
  "\n"
  "ASSIGNED {\n"
  "	ik		(mA/cm2)\n"
  "	oinf\n"
  "	tau		(ms)\n"
  "}\n"
  "\n"
  "STATE {	o }		: fraction of open channels\n"
  "\n"
  "BREAKPOINT {\n"
  "	SOLVE state\n"
  "	ik = gkbar*o*(v - ek) : potassium current induced by this channel\n"
  "}\n"
  "\n"
  "LOCAL fac\n"
  "\n"
  ":if state_cagk is called from hoc, garbage or segmentation violation will\n"
  ":result because range variables won't have correct pointer.  This is because\n"
  ":only BREAKPOINT sets up the correct pointers to range variables.\n"
  "PROCEDURE state() {	: exact when v held constant; integrates over dt step\n"
  "	rate(v, cai)\n"
  "	o = o + fac*(oinf - o)\n"
  "	VERBATIM\n"
  "	return 0;\n"
  "	ENDVERBATIM\n"
  "}\n"
  "\n"
  "INITIAL {           : initialize the following parameter using rate()\n"
  "	rate(v, cai)\n"
  "	o = oinf\n"
  "}\n"
  "\n"
  "FUNCTION alp(v (mV), ca (mM)) (1/ms) { :callable from hoc\n"
  "	alp = abar/(1 + exp1(k1,d1,v)/ca)\n"
  "}\n"
  "\n"
  "FUNCTION bet(v (mV), ca (mM)) (1/ms) { :callable from hoc\n"
  "	bet = bbar/(1 + ca/exp1(k2,d2,v))\n"
  "}  \n"
  "\n"
  "FUNCTION exp1(k (mM), d, v (mV)) (mM) { :callable from hoc\n"
  "	exp1 = k*exp(-2*d*FARADAY*v/R/(273.15 + celsius))\n"
  "}\n"
  "\n"
  "PROCEDURE rate(v (mV), ca (mM)) { :callable from hoc\n"
  "	LOCAL a\n"
  "	a = alp(v,ca)\n"
  "	tau = 1/(a + bet(v, ca)) : estimation of activation tau\n"
  "	oinf = a*tau             : estimation of activation steady state value\n"
  "	fac = (1 - exp(-dt/tau))\n"
  "}\n"
  ;
    hoc_reg_nmodl_filename(mech_type, nmodl_filename);
    hoc_reg_nmodl_text(mech_type, nmodl_file_text);
}
#endif
