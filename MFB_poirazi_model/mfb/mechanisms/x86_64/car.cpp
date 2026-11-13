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
static constexpr auto number_of_datum_variables = 3;
static constexpr auto number_of_floating_point_variables = 11;
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
 
#define nrn_init _nrn_init__car
#define _nrn_initial _nrn_initial__car
#define nrn_cur _nrn_cur__car
#define _nrn_current _nrn_current__car
#define nrn_jacob _nrn_jacob__car
#define nrn_state _nrn_state__car
#define _net_receive _net_receive__car 
#define calcg calcg__car 
#define mhn mhn__car 
#define states states__car 
 
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
#define gcabar _ml->template fpfield<0>(_iml)
#define gcabar_columnindex 0
#define inf _ml->template data_array<1, 2>(_iml)
#define inf_columnindex 1
#define fac _ml->template data_array<2, 2>(_iml)
#define fac_columnindex 2
#define tau _ml->template data_array<3, 2>(_iml)
#define tau_columnindex 3
#define m _ml->template fpfield<4>(_iml)
#define m_columnindex 4
#define h _ml->template fpfield<5>(_iml)
#define h_columnindex 5
#define eca _ml->template fpfield<6>(_iml)
#define eca_columnindex 6
#define Dm _ml->template fpfield<7>(_iml)
#define Dm_columnindex 7
#define Dh _ml->template fpfield<8>(_iml)
#define Dh_columnindex 8
#define ica _ml->template fpfield<9>(_iml)
#define ica_columnindex 9
#define _g _ml->template fpfield<10>(_iml)
#define _g_columnindex 10
#define _ion_eca *(_ml->dptr_field<0>(_iml))
#define _p_ion_eca static_cast<neuron::container::data_handle<double>>(_ppvar[0])
#define _ion_ica *(_ml->dptr_field<1>(_iml))
#define _p_ion_ica static_cast<neuron::container::data_handle<double>>(_ppvar[1])
#define _ion_dicadv *(_ml->dptr_field<2>(_iml))
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
 {"setdata_car", _hoc_setdata},
 {"calcg_car", _hoc_calcg},
 {"mhn_car", _hoc_mhn},
 {"states_car", _hoc_states},
 {"vartau_car", _hoc_vartau},
 {"varss_car", _hoc_varss},
 {0, 0}
};
 
/* Direct Python call wrappers to density mechanism functions.*/
 static double _npy_calcg(Prop*);
 static double _npy_mhn(Prop*);
 static double _npy_states(Prop*);
 static double _npy_vartau(Prop*);
 static double _npy_varss(Prop*);
 
static NPyDirectMechFunc npy_direct_func_proc[] = {
 {"calcg", _npy_calcg},
 {"mhn", _npy_mhn},
 {"states", _npy_states},
 {"vartau", _npy_vartau},
 {"varss", _npy_varss},
 {0, 0}
};
#define vartau vartau_car
#define varss varss_car
 extern double vartau( double , double );
 extern double varss( double , double );
 /* declare global and static user variables */
 #define gind 0
 #define _gth 0
 /* some parameters have upper and lower limits */
 static HocParmLimits _hoc_parm_limits[] = {
 {0, 0, 0}
};
 static HocParmUnits _hoc_parm_units[] = {
 {"gcabar_car", "mho/cm2"},
 {0, 0}
};
 static double delta_t = 0.01;
 static double h0 = 0;
 static double m0 = 0;
 static double v = 0;
 /* connect global user variables to hoc */
 static DoubScal hoc_scdoub[] = {
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
"car",
 "gcabar_car",
 0,
 "inf_car[2]",
 "fac_car[2]",
 "tau_car[2]",
 0,
 "m_car",
 "h_car",
 0,
 0};
 static Symbol* _ca_sym;
 
 /* Used by NrnProperty */
 static _nrn_mechanism_std_vector<double> _parm_default{
     0, /* gcabar */
 }; 
 
 
extern Prop* need_memb(Symbol*);
static void nrn_alloc(Prop* _prop) {
  Prop *prop_ion{};
  Datum *_ppvar{};
   _ppvar = nrn_prop_datum_alloc(_mechtype, 3, _prop);
    _nrn_mechanism_access_dparam(_prop) = _ppvar;
     _nrn_mechanism_cache_instance _ml_real{_prop};
    auto* const _ml = &_ml_real;
    size_t const _iml{};
    assert(_nrn_mechanism_get_num_vars(_prop) == 11);
 	/*initialize range parameters*/
 	gcabar = _parm_default[0]; /* 0 */
 	 assert(_nrn_mechanism_get_num_vars(_prop) == 11);
 	_nrn_mechanism_access_dparam(_prop) = _ppvar;
 	/*connect ionic variables to this model*/
 prop_ion = need_memb(_ca_sym);
 nrn_promote(prop_ion, 0, 1);
 	_ppvar[0] = _nrn_mechanism_get_param_handle(prop_ion, 0); /* eca */
 	_ppvar[1] = _nrn_mechanism_get_param_handle(prop_ion, 3); /* ica */
 	_ppvar[2] = _nrn_mechanism_get_param_handle(prop_ion, 4); /* _ion_dicadv */
 
}
 static void _initlists();
 extern Symbol* hoc_lookup(const char*);
extern void _nrn_thread_reg(int, int, void(*)(Datum*));
void _nrn_thread_table_reg(int, nrn_thread_table_check_t);
extern void hoc_register_tolerance(int, HocStateTolerance*, Symbol***);
extern void _cvode_abstol( Symbol**, double*, int);

 extern "C" void _car_reg() {
	int _vectorized = 0;
  _initlists();
 	ion_reg("ca", -10000.);
 	_ca_sym = hoc_lookup("ca_ion");
 	register_mech(_mechanism, nrn_alloc,nrn_cur, nrn_jacob, nrn_state, nrn_init, hoc_nrnpointerindex, 0);
 _mechtype = nrn_get_mechtype(_mechanism[1]);
 hoc_register_parm_default(_mechtype, &_parm_default);
         hoc_register_npy_direct(_mechtype, npy_direct_func_proc);
     _nrn_setdata_reg(_mechtype, _setdata);
 #if NMODL_TEXT
  register_nmodl_text_and_filename(_mechtype);
#endif
   _nrn_mechanism_register_data_fields(_mechtype,
                                       _nrn_mechanism_field<double>{"gcabar"} /* 0 */,
                                       _nrn_mechanism_field<double>{"inf", 2} /* 1 */,
                                       _nrn_mechanism_field<double>{"fac", 2} /* 2 */,
                                       _nrn_mechanism_field<double>{"tau", 2} /* 3 */,
                                       _nrn_mechanism_field<double>{"m"} /* 4 */,
                                       _nrn_mechanism_field<double>{"h"} /* 5 */,
                                       _nrn_mechanism_field<double>{"eca"} /* 6 */,
                                       _nrn_mechanism_field<double>{"Dm"} /* 7 */,
                                       _nrn_mechanism_field<double>{"Dh"} /* 8 */,
                                       _nrn_mechanism_field<double>{"ica"} /* 9 */,
                                       _nrn_mechanism_field<double>{"_g"} /* 10 */,
                                       _nrn_mechanism_field<double*>{"_ion_eca", "ca_ion"} /* 0 */,
                                       _nrn_mechanism_field<double*>{"_ion_ica", "ca_ion"} /* 1 */,
                                       _nrn_mechanism_field<double*>{"_ion_dicadv", "ca_ion"} /* 2 */);
  hoc_register_prop_size(_mechtype, 14, 3);
  hoc_register_dparam_semantics(_mechtype, 0, "ca_ion");
  hoc_register_dparam_semantics(_mechtype, 1, "ca_ion");
  hoc_register_dparam_semantics(_mechtype, 2, "ca_ion");
 	hoc_register_cvode(_mechtype, _ode_count, 0, 0, 0);
 
    hoc_register_var(hoc_scdoub, hoc_vdoub, hoc_intfunc);
 	ivoc_help("help ?1 car /home/nishant/lab/project_MFB/MFB_poirazi_model/mfb/mechanisms/car.mod\n");
 hoc_register_limits(_mechtype, _hoc_parm_limits);
 hoc_register_units(_mechtype, _hoc_parm_units);
 }
static int _reset;
static const char *modelname = "Ca R-type channel with medium threshold for activation";

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
    return 0; }
 
static void _hoc_calcg(void) {
  double _r;
  
  if(!_prop_id) {
    hoc_execerror("No data for calcg_car. Requires prior call to setdata_car and that the specified mechanism instance still be in existence.", NULL);
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
    hoc_execerror("No data for states_car. Requires prior call to setdata_car and that the specified mechanism instance still be in existence.", NULL);
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
     _lvarss = 1.0 / ( 1.0 + exp ( ( _lv + 48.5 ) / ( - 3.0 ) ) ) ;
     }
   else if ( _li  == 1.0 ) {
     _lvarss = 1.0 / ( 1.0 + exp ( ( _lv + 53.0 ) / ( 1.0 ) ) ) ;
     }
   
return _lvarss;
 }
 
static void _hoc_varss(void) {
  double _r;
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
 
double vartau (  double _lv , double _li ) {
   double _lvartau;
 if ( _li  == 0.0 ) {
     _lvartau = 50.0 ;
     }
   else if ( _li  == 1.0 ) {
     _lvartau = 5.0 ;
     }
   
return _lvartau;
 }
 
static void _hoc_vartau(void) {
  double _r;
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
 {int  _li ;for ( _li = 0 ; _li <= 1 ; _li ++ ) {
     tau [ _li ] = vartau ( _threadargscomma_ _lv , ((double) _li ) ) ;
     inf [ _li ] = varss ( _threadargscomma_ _lv , ((double) _li ) ) ;
     fac [ _li ] = ( 1.0 - exp ( - dt / tau [ _li ] ) ) ;
     } }
    return 0; }
 
static void _hoc_mhn(void) {
  double _r;
  
  if(!_prop_id) {
    hoc_execerror("No data for mhn_car. Requires prior call to setdata_car and that the specified mechanism instance still be in existence.", NULL);
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
 
static int _ode_count(int _type){ hoc_execerror("car", "cannot be used with CVODE"); return 0;}

static void initmodel() {
  int _i; double _save;_ninits++;
 _save = t;
 t = 0.0;
{
  h = h0;
  m = m0;
 {
   m = 0.0 ;
   h = 1.0 ;
   states ( _threadargs_ ) ;
   ica = gcabar * m * m * m * h * ( v - eca ) ;
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
  eca = _ion_eca;
 initmodel();
 }}

static double _nrn_current(double _v){double _current=0.;v=_v;{ {
   ica = gcabar * m * m * m * h * ( v - eca ) ;
   }
 _current += ica;

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
  eca = _ion_eca;
 auto const _g_local = _nrn_current(_v + .001);
 	{ double _dica;
  _dica = ica;
 _rhs = _nrn_current(_v);
  _ion_dicadv += (_dica - ica)/.001 ;
 	}
 _g = (_g_local - _rhs)/.001;
  _ion_ica += ica ;
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
  eca = _ion_eca;
 { error =  states();
 if(error){
  std_cerr_stream << "at line 39 in file car.mod:\n	SOLVE states\n";
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
    const char* nmodl_filename = "/home/nishant/lab/project_MFB/MFB_poirazi_model/mfb/mechanisms/car.mod";
    const char* nmodl_file_text = 
  "TITLE Ca R-type channel with medium threshold for activation\n"
  ": used in distal dendritic regions, together with calH.mod, to help\n"
  ": the generation of Ca++ spikes in these regions\n"
  ": uses channel conductance (not permeability)\n"
  ": written by Yiota Poirazi on 11/13/00 poirazi@LNC.usc.edu\n"
  "\n"
  "NEURON {\n"
  "	SUFFIX car\n"
  "	USEION ca READ eca WRITE ica\n"
  "        RANGE gcabar, m, h\n"
  "	RANGE inf, fac, tau\n"
  "}\n"
  "\n"
  "UNITS {\n"
  "	(mA) = (milliamp)\n"
  "	(mV) = (millivolt)\n"
  "}\n"
  "\n"
  "INDEPENDENT {t FROM 0 TO 1 WITH 1 (ms)}\n"
  "\n"
  "PARAMETER {              : parameters that can be entered when function is called in cell-setup\n"
  "        v               (mV)\n"
  "        celsius = 34	(degC)\n"
  "	dt              (ms)\n"
  "        gcabar = 0      (mho/cm2) : initialized conductance\n"
  "	eca = 140       (mV)      : Ca++ reversal potential\n"
  "        }  \n"
  "\n"
  "STATE {	m h }            : unknown activation and inactivation parameters to be solved in the DEs  \n"
  "\n"
  "ASSIGNED {               : parameters needed to solve DE\n"
  "	ica (mA/cm2)\n"
  "        inf[2]\n"
  "	fac[2]\n"
  "	tau[2]\n"
  "}\n"
  "\n"
  "BREAKPOINT {\n"
  "	SOLVE states\n"
  "	ica = gcabar*m*m*m*h*(v - eca)\n"
  "	}\n"
  "\n"
  "INITIAL {\n"
  "        m = 0    : initial activation parameter value\n"
  "	h = 1    : initial inactivation parameter value\n"
  "	states()\n"
  "	ica = gcabar*m*m*m*h*(v - eca) : initial Ca++ current value\n"
  "        }\n"
  "\n"
  "PROCEDURE calcg() {\n"
  "	mhn(v*1(/mV))\n"
  "	m = m + fac[0]*(inf[0] - m)\n"
  "	h = h + fac[1]*(inf[1] - h)\n"
  "	}	\n"
  "\n"
  "PROCEDURE states() {	: exact when v held constant\n"
  "	calcg()\n"
  "	VERBATIM\n"
  "	return 0;\n"
  "	ENDVERBATIM\n"
  "}\n"
  "\n"
  "FUNCTION varss(v, i) {\n"
  "	if (i==0) {\n"
  "	    varss = 1 / (1 + exp((v+48.5)/(-3))) : Ca activation\n"
  "	}\n"
  "	else if (i==1) {\n"
  "             varss = 1/ (1 + exp((v+53)/(1)))    : Ca inactivation\n"
  "	}\n"
  "}\n"
  "\n"
  "FUNCTION vartau(v, i) {\n"
  "	if (i==0) {\n"
  "           vartau = 50  : activation variable time constant\n"
  "        }\n"
  "	else if (i==1) {\n"
  "           vartau = 5   : inactivation variable time constant\n"
  "       }\n"
  "	\n"
  "}	\n"
  "\n"
  "PROCEDURE mhn(v) {LOCAL a, b :rest = -70\n"
  ":	TABLE inf, fac DEPEND dt, celsius FROM -100 TO 100 WITH 200\n"
  "	FROM i=0 TO 1 {\n"
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
