/* Created by Language version: 7.7.0 */
/* VECTORIZED */
#define NRN_VECTORIZED 1
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
static constexpr auto number_of_datum_variables = 2;
static constexpr auto number_of_floating_point_variables = 28;
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
 
#define nrn_init _nrn_init__MFBSyn
#define _nrn_initial _nrn_initial__MFBSyn
#define nrn_cur _nrn_cur__MFBSyn
#define _nrn_current _nrn_current__MFBSyn
#define nrn_jacob _nrn_jacob__MFBSyn
#define nrn_state _nrn_state__MFBSyn
#define _net_receive _net_receive__MFBSyn 
#define state state__MFBSyn 
 
#define _threadargscomma_ _ml, _iml, _ppvar, _thread, _globals, _nt,
#define _threadargsprotocomma_ Memb_list* _ml, size_t _iml, Datum* _ppvar, Datum* _thread, double* _globals, NrnThread* _nt,
#define _internalthreadargsprotocomma_ _nrn_mechanism_cache_range* _ml, size_t _iml, Datum* _ppvar, Datum* _thread, double* _globals, NrnThread* _nt,
#define _threadargs_ _ml, _iml, _ppvar, _thread, _globals, _nt
#define _threadargsproto_ Memb_list* _ml, size_t _iml, Datum* _ppvar, Datum* _thread, double* _globals, NrnThread* _nt
#define _internalthreadargsproto_ _nrn_mechanism_cache_range* _ml, size_t _iml, Datum* _ppvar, Datum* _thread, double* _globals, NrnThread* _nt
 	/*SUPPRESS 761*/
	/*SUPPRESS 762*/
	/*SUPPRESS 763*/
	/*SUPPRESS 765*/
	 extern double *hoc_getarg(int);
 
#define t _nt->_t
#define dt _nt->_dt
#define gq_ampa _ml->template fpfield<0>(_iml)
#define gq_ampa_columnindex 0
#define tau_r_ampa _ml->template fpfield<1>(_iml)
#define tau_r_ampa_columnindex 1
#define tau_d_ampa _ml->template fpfield<2>(_iml)
#define tau_d_ampa_columnindex 2
#define nmda_ratio _ml->template fpfield<3>(_iml)
#define nmda_ratio_columnindex 3
#define tau_r_nmda _ml->template fpfield<4>(_iml)
#define tau_r_nmda_columnindex 4
#define tau_d_nmda _ml->template fpfield<5>(_iml)
#define tau_d_nmda_columnindex 5
#define mg _ml->template fpfield<6>(_iml)
#define mg_columnindex 6
#define e _ml->template fpfield<7>(_iml)
#define e_columnindex 7
#define i _ml->template fpfield<8>(_iml)
#define i_columnindex 8
#define i_ampa _ml->template fpfield<9>(_iml)
#define i_ampa_columnindex 9
#define i_nmda _ml->template fpfield<10>(_iml)
#define i_nmda_columnindex 10
#define g_ampa _ml->template fpfield<11>(_iml)
#define g_ampa_columnindex 11
#define g_nmda _ml->template fpfield<12>(_iml)
#define g_nmda_columnindex 12
#define mgblock _ml->template fpfield<13>(_iml)
#define mgblock_columnindex 13
#define nev _ml->template fpfield<14>(_iml)
#define nev_columnindex 14
#define A1 _ml->template fpfield<15>(_iml)
#define A1_columnindex 15
#define A2 _ml->template fpfield<16>(_iml)
#define A2_columnindex 16
#define B1 _ml->template fpfield<17>(_iml)
#define B1_columnindex 17
#define B2 _ml->template fpfield<18>(_iml)
#define B2_columnindex 18
#define f_ampa _ml->template fpfield<19>(_iml)
#define f_ampa_columnindex 19
#define f_nmda _ml->template fpfield<20>(_iml)
#define f_nmda_columnindex 20
#define DA1 _ml->template fpfield<21>(_iml)
#define DA1_columnindex 21
#define DA2 _ml->template fpfield<22>(_iml)
#define DA2_columnindex 22
#define DB1 _ml->template fpfield<23>(_iml)
#define DB1_columnindex 23
#define DB2 _ml->template fpfield<24>(_iml)
#define DB2_columnindex 24
#define v _ml->template fpfield<25>(_iml)
#define v_columnindex 25
#define _g _ml->template fpfield<26>(_iml)
#define _g_columnindex 26
#define _tsav _ml->template fpfield<27>(_iml)
#define _tsav_columnindex 27
#define _nd_area *_ml->dptr_field<0>(_iml)
 /* Thread safe. No static _ml, _iml or _ppvar. */
 static int hoc_nrnpointerindex =  -1;
 static _nrn_mechanism_std_vector<Datum> _extcall_thread;
 /* external NEURON variables */
 /* declaration of user functions */
 static double _hoc_peaknorm(void*);
 static int _mechtype;
extern void _nrn_cacheloop_reg(int, int);
extern void hoc_register_limits(int, HocParmLimits*);
extern void hoc_register_units(int, HocParmUnits*);
extern void nrn_promote(Prop*, int, int);
 
#define NMODL_TEXT 1
#if NMODL_TEXT
static void register_nmodl_text_and_filename(int mechtype);
#endif
 extern Prop* nrn_point_prop_;
 static int _pointtype;
 static void* _hoc_create_pnt(Object* _ho) { void* create_point_process(int, Object*);
 return create_point_process(_pointtype, _ho);
}
 static void _hoc_destroy_pnt(void*);
 static double _hoc_loc_pnt(void* _vptr) {double loc_point_process(int, void*);
 return loc_point_process(_pointtype, _vptr);
}
 static double _hoc_has_loc(void* _vptr) {double has_loc_point(void*);
 return has_loc_point(_vptr);
}
 static double _hoc_get_loc_pnt(void* _vptr) {
 double get_loc_point_process(void*); return (get_loc_point_process(_vptr));
}
 static void _hoc_setdata(void*);
 /* connect user functions to hoc names */
 static VoidFunc hoc_intfunc[] = {
 {0, 0}
};
 static Member_func _member_func[] = {
 {"loc", _hoc_loc_pnt},
 {"has_loc", _hoc_has_loc},
 {"get_loc", _hoc_get_loc_pnt},
 {"peaknorm", _hoc_peaknorm},
 {0, 0}
};
#define peaknorm peaknorm_MFBSyn
 extern double peaknorm( _internalthreadargsprotocomma_ double , double );
 /* declare global and static user variables */
 #define gind 0
 #define _gth 0
 /* some parameters have upper and lower limits */
 static HocParmLimits _hoc_parm_limits[] = {
 {0, 0, 0}
};
 static HocParmUnits _hoc_parm_units[] = {
 {"gq_ampa", "uS"},
 {"tau_r_ampa", "ms"},
 {"tau_d_ampa", "ms"},
 {"nmda_ratio", "1"},
 {"tau_r_nmda", "ms"},
 {"tau_d_nmda", "ms"},
 {"mg", "mM"},
 {"e", "mV"},
 {"A1", "uS"},
 {"A2", "uS"},
 {"B1", "uS"},
 {"B2", "uS"},
 {"i", "nA"},
 {"i_ampa", "nA"},
 {"i_nmda", "nA"},
 {"g_ampa", "uS"},
 {"g_nmda", "uS"},
 {"mgblock", "1"},
 {"nev", "1"},
 {0, 0}
};
 static double A20 = 0;
 static double A10 = 0;
 static double B20 = 0;
 static double B10 = 0;
 static double delta_t = 0.01;
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
 }
 static void _hoc_setdata(void* _vptr) { Prop* _prop;
 _prop = ((Point_process*)_vptr)->_prop;
   _setdata(_prop);
 }
 static void nrn_alloc(Prop*);
static void nrn_init(_nrn_model_sorted_token const&, NrnThread*, Memb_list*, int);
static void nrn_state(_nrn_model_sorted_token const&, NrnThread*, Memb_list*, int);
 static void nrn_cur(_nrn_model_sorted_token const&, NrnThread*, Memb_list*, int);
static void nrn_jacob(_nrn_model_sorted_token const&, NrnThread*, Memb_list*, int);
 static void _hoc_destroy_pnt(void* _vptr) {
   destroy_point_process(_vptr);
}
 
static int _ode_count(int);
static void _ode_map(Prop*, int, neuron::container::data_handle<double>*, neuron::container::data_handle<double>*, double*, int);
static void _ode_spec(_nrn_model_sorted_token const&, NrnThread*, Memb_list*, int);
static void _ode_matsol(_nrn_model_sorted_token const&, NrnThread*, Memb_list*, int);
 
#define _cvode_ieq _ppvar[2].literal_value<int>()
 static void _ode_matsol_instance1(_internalthreadargsproto_);
 /* connect range variables in _p that hoc is supposed to know about */
 static const char *_mechanism[] = {
 "7.7.0",
"MFBSyn",
 "gq_ampa",
 "tau_r_ampa",
 "tau_d_ampa",
 "nmda_ratio",
 "tau_r_nmda",
 "tau_d_nmda",
 "mg",
 "e",
 0,
 "i",
 "i_ampa",
 "i_nmda",
 "g_ampa",
 "g_nmda",
 "mgblock",
 "nev",
 0,
 "A1",
 "A2",
 "B1",
 "B2",
 0,
 0};
 
 /* Used by NrnProperty */
 static _nrn_mechanism_std_vector<double> _parm_default{
     0.0005, /* gq_ampa */
     0.5, /* tau_r_ampa */
     5, /* tau_d_ampa */
     0.3, /* nmda_ratio */
     3, /* tau_r_nmda */
     70, /* tau_d_nmda */
     1, /* mg */
     0, /* e */
 }; 
 
 
extern Prop* need_memb(Symbol*);
static void nrn_alloc(Prop* _prop) {
  Prop *prop_ion{};
  Datum *_ppvar{};
  if (nrn_point_prop_) {
    _nrn_mechanism_access_alloc_seq(_prop) = _nrn_mechanism_access_alloc_seq(nrn_point_prop_);
    _ppvar = _nrn_mechanism_access_dparam(nrn_point_prop_);
  } else {
   _ppvar = nrn_prop_datum_alloc(_mechtype, 3, _prop);
    _nrn_mechanism_access_dparam(_prop) = _ppvar;
     _nrn_mechanism_cache_instance _ml_real{_prop};
    auto* const _ml = &_ml_real;
    size_t const _iml{};
    assert(_nrn_mechanism_get_num_vars(_prop) == 28);
 	/*initialize range parameters*/
 	gq_ampa = _parm_default[0]; /* 0.0005 */
 	tau_r_ampa = _parm_default[1]; /* 0.5 */
 	tau_d_ampa = _parm_default[2]; /* 5 */
 	nmda_ratio = _parm_default[3]; /* 0.3 */
 	tau_r_nmda = _parm_default[4]; /* 3 */
 	tau_d_nmda = _parm_default[5]; /* 70 */
 	mg = _parm_default[6]; /* 1 */
 	e = _parm_default[7]; /* 0 */
  }
 	 assert(_nrn_mechanism_get_num_vars(_prop) == 28);
 	_nrn_mechanism_access_dparam(_prop) = _ppvar;
 	/*connect ionic variables to this model*/
 
}
 static void _initlists();
  /* some states have an absolute tolerance */
 static Symbol** _atollist;
 static HocStateTolerance _hoc_state_tol[] = {
 {0, 0}
};
 static void _net_receive(Point_process*, double*, double);
 extern Symbol* hoc_lookup(const char*);
extern void _nrn_thread_reg(int, int, void(*)(Datum*));
void _nrn_thread_table_reg(int, nrn_thread_table_check_t);
extern void hoc_register_tolerance(int, HocStateTolerance*, Symbol***);
extern void _cvode_abstol( Symbol**, double*, int);

 extern "C" void _mfbsyn_reg() {
	int _vectorized = 1;
  _initlists();
 	_pointtype = point_register_mech(_mechanism,
	 nrn_alloc,nrn_cur, nrn_jacob, nrn_state, nrn_init,
	 hoc_nrnpointerindex, 1,
	 _hoc_create_pnt, _hoc_destroy_pnt, _member_func);
 _mechtype = nrn_get_mechtype(_mechanism[1]);
 hoc_register_parm_default(_mechtype, &_parm_default);
     _nrn_setdata_reg(_mechtype, _setdata);
 #if NMODL_TEXT
  register_nmodl_text_and_filename(_mechtype);
#endif
   _nrn_mechanism_register_data_fields(_mechtype,
                                       _nrn_mechanism_field<double>{"gq_ampa"} /* 0 */,
                                       _nrn_mechanism_field<double>{"tau_r_ampa"} /* 1 */,
                                       _nrn_mechanism_field<double>{"tau_d_ampa"} /* 2 */,
                                       _nrn_mechanism_field<double>{"nmda_ratio"} /* 3 */,
                                       _nrn_mechanism_field<double>{"tau_r_nmda"} /* 4 */,
                                       _nrn_mechanism_field<double>{"tau_d_nmda"} /* 5 */,
                                       _nrn_mechanism_field<double>{"mg"} /* 6 */,
                                       _nrn_mechanism_field<double>{"e"} /* 7 */,
                                       _nrn_mechanism_field<double>{"i"} /* 8 */,
                                       _nrn_mechanism_field<double>{"i_ampa"} /* 9 */,
                                       _nrn_mechanism_field<double>{"i_nmda"} /* 10 */,
                                       _nrn_mechanism_field<double>{"g_ampa"} /* 11 */,
                                       _nrn_mechanism_field<double>{"g_nmda"} /* 12 */,
                                       _nrn_mechanism_field<double>{"mgblock"} /* 13 */,
                                       _nrn_mechanism_field<double>{"nev"} /* 14 */,
                                       _nrn_mechanism_field<double>{"A1"} /* 15 */,
                                       _nrn_mechanism_field<double>{"A2"} /* 16 */,
                                       _nrn_mechanism_field<double>{"B1"} /* 17 */,
                                       _nrn_mechanism_field<double>{"B2"} /* 18 */,
                                       _nrn_mechanism_field<double>{"f_ampa"} /* 19 */,
                                       _nrn_mechanism_field<double>{"f_nmda"} /* 20 */,
                                       _nrn_mechanism_field<double>{"DA1"} /* 21 */,
                                       _nrn_mechanism_field<double>{"DA2"} /* 22 */,
                                       _nrn_mechanism_field<double>{"DB1"} /* 23 */,
                                       _nrn_mechanism_field<double>{"DB2"} /* 24 */,
                                       _nrn_mechanism_field<double>{"v"} /* 25 */,
                                       _nrn_mechanism_field<double>{"_g"} /* 26 */,
                                       _nrn_mechanism_field<double>{"_tsav"} /* 27 */,
                                       _nrn_mechanism_field<double*>{"_nd_area", "area"} /* 0 */,
                                       _nrn_mechanism_field<Point_process*>{"_pntproc", "pntproc"} /* 1 */,
                                       _nrn_mechanism_field<int>{"_cvode_ieq", "cvodeieq"} /* 2 */);
  hoc_register_prop_size(_mechtype, 28, 3);
  hoc_register_dparam_semantics(_mechtype, 0, "area");
  hoc_register_dparam_semantics(_mechtype, 1, "pntproc");
  hoc_register_dparam_semantics(_mechtype, 2, "cvodeieq");
 	hoc_register_cvode(_mechtype, _ode_count, _ode_map, _ode_spec, _ode_matsol);
 	hoc_register_tolerance(_mechtype, _hoc_state_tol, &_atollist);
 pnt_receive[_mechtype] = _net_receive;
 pnt_receive_size[_mechtype] = 1;
 
    hoc_register_var(hoc_scdoub, hoc_vdoub, hoc_intfunc);
 	ivoc_help("help ?1 MFBSyn /home/nishant/lab/project_MFB/MFB_poirazi_model/mfb/mechanisms/mfbsyn.mod\n");
 hoc_register_limits(_mechtype, _hoc_parm_limits);
 hoc_register_units(_mechtype, _hoc_parm_units);
 }
static int _reset;
static const char *modelname = "";

static int error;
static int _ninits = 0;
static int _match_recurse=1;
static void _modl_cleanup(){ _match_recurse=1;}
 
static int _ode_spec1(_internalthreadargsproto_);
/*static int _ode_matsol1(_internalthreadargsproto_);*/
 static neuron::container::field_index _slist1[4], _dlist1[4];
 static int state(_internalthreadargsproto_);
 
/*CVODE*/
 static int _ode_spec1 (_internalthreadargsproto_) {int _reset = 0; {
   DA1 = - A1 / tau_r_ampa ;
   DA2 = - A2 / tau_d_ampa ;
   DB1 = - B1 / tau_r_nmda ;
   DB2 = - B2 / tau_d_nmda ;
   }
 return _reset;
}
 static int _ode_matsol1 (_internalthreadargsproto_) {
 DA1 = DA1  / (1. - dt*( ( - 1.0 ) / tau_r_ampa )) ;
 DA2 = DA2  / (1. - dt*( ( - 1.0 ) / tau_d_ampa )) ;
 DB1 = DB1  / (1. - dt*( ( - 1.0 ) / tau_r_nmda )) ;
 DB2 = DB2  / (1. - dt*( ( - 1.0 ) / tau_d_nmda )) ;
  return 0;
}
 /*END CVODE*/
 static int state (_internalthreadargsproto_) { {
    A1 = A1 + (1. - exp(dt*(( - 1.0 ) / tau_r_ampa)))*(- ( 0.0 ) / ( ( - 1.0 ) / tau_r_ampa ) - A1) ;
    A2 = A2 + (1. - exp(dt*(( - 1.0 ) / tau_d_ampa)))*(- ( 0.0 ) / ( ( - 1.0 ) / tau_d_ampa ) - A2) ;
    B1 = B1 + (1. - exp(dt*(( - 1.0 ) / tau_r_nmda)))*(- ( 0.0 ) / ( ( - 1.0 ) / tau_r_nmda ) - B1) ;
    B2 = B2 + (1. - exp(dt*(( - 1.0 ) / tau_d_nmda)))*(- ( 0.0 ) / ( ( - 1.0 ) / tau_d_nmda ) - B2) ;
   }
  return 0;
}
 
double peaknorm ( _internalthreadargsprotocomma_ double _ltr , double _ltd ) {
   double _lpeaknorm;
 double _ltp ;
 _ltp = ( _ltr * _ltd ) / ( _ltd - _ltr ) * log ( _ltd / _ltr ) ;
   _lpeaknorm = 1.0 / ( - exp ( - _ltp / _ltr ) + exp ( - _ltp / _ltd ) ) ;
   
return _lpeaknorm;
 }
 
static double _hoc_peaknorm(void* _vptr) {
 double _r;
 Datum* _ppvar; Datum* _thread; NrnThread* _nt;
   auto* const _pnt = static_cast<Point_process*>(_vptr);
  auto* const _p = _pnt->_prop;
  if (!_p) {
    hoc_execerror("POINT_PROCESS data instance not valid", NULL);
  }
   _nrn_mechanism_cache_instance _ml_real{_p};
  auto* const _ml = &_ml_real;
  size_t const _iml{};
  _ppvar = _nrn_mechanism_access_dparam(_p);
  _thread = _extcall_thread.data();
  double* _globals = nullptr;
  if (gind != 0 && _thread != nullptr) { _globals = _thread[_gth].get<double*>(); }
  _nt = static_cast<NrnThread*>(_pnt->_vnt);
 _r =  peaknorm ( _threadargscomma_ *getarg(1) , *getarg(2) );
 return(_r);
}
 
static void _net_receive (Point_process* _pnt, double* _args, double _lflag) 
{  Prop* _p; Datum* _ppvar; Datum* _thread; NrnThread* _nt;
   _nrn_mechanism_cache_instance _ml_real{_pnt->_prop};
  auto* const _ml = &_ml_real;
  size_t const _iml{};
   _thread = nullptr; double* _globals = nullptr; _nt = (NrnThread*)_pnt->_vnt;   _ppvar = _nrn_mechanism_access_dparam(_pnt->_prop);
  if (_tsav > t){ hoc_execerror(hoc_object_name(_pnt->ob), ":Event arrived out of order. Must call ParallelContext.set_maxstep AFTER assigning minimum NetCon.delay");}
 _tsav = t; {
     if (nrn_netrec_state_adjust && !cvode_active_){
    /* discon state adjustment for cnexp case (rate uses no local variable) */
    double __state = A1;
    double __primary = (A1 + _args[0] * gq_ampa * f_ampa) - __state;
     __primary += ( 1. - exp( 0.5*dt*( ( - 1.0 ) / tau_r_ampa ) ) )*( - ( 0.0 ) / ( ( - 1.0 ) / tau_r_ampa ) - __primary );
    A1 += __primary;
  } else {
 A1 = A1 + _args[0] * gq_ampa * f_ampa ;
     }
   if (nrn_netrec_state_adjust && !cvode_active_){
    /* discon state adjustment for cnexp case (rate uses no local variable) */
    double __state = A2;
    double __primary = (A2 + _args[0] * gq_ampa * f_ampa) - __state;
     __primary += ( 1. - exp( 0.5*dt*( ( - 1.0 ) / tau_d_ampa ) ) )*( - ( 0.0 ) / ( ( - 1.0 ) / tau_d_ampa ) - __primary );
    A2 += __primary;
  } else {
 A2 = A2 + _args[0] * gq_ampa * f_ampa ;
     }
   if (nrn_netrec_state_adjust && !cvode_active_){
    /* discon state adjustment for cnexp case (rate uses no local variable) */
    double __state = B1;
    double __primary = (B1 + _args[0] * nmda_ratio * gq_ampa * f_nmda) - __state;
     __primary += ( 1. - exp( 0.5*dt*( ( - 1.0 ) / tau_r_nmda ) ) )*( - ( 0.0 ) / ( ( - 1.0 ) / tau_r_nmda ) - __primary );
    B1 += __primary;
  } else {
 B1 = B1 + _args[0] * nmda_ratio * gq_ampa * f_nmda ;
     }
   if (nrn_netrec_state_adjust && !cvode_active_){
    /* discon state adjustment for cnexp case (rate uses no local variable) */
    double __state = B2;
    double __primary = (B2 + _args[0] * nmda_ratio * gq_ampa * f_nmda) - __state;
     __primary += ( 1. - exp( 0.5*dt*( ( - 1.0 ) / tau_d_nmda ) ) )*( - ( 0.0 ) / ( ( - 1.0 ) / tau_d_nmda ) - __primary );
    B2 += __primary;
  } else {
 B2 = B2 + _args[0] * nmda_ratio * gq_ampa * f_nmda ;
     }
 nev = nev + _args[0] ;
   } }
 
static int _ode_count(int _type){ return 4;}
 
static void _ode_spec(_nrn_model_sorted_token const& _sorted_token, NrnThread* _nt, Memb_list* _ml_arg, int _type) {
   Datum* _ppvar;
   size_t _iml;   _nrn_mechanism_cache_range* _ml;   Node* _nd{};
  double _v{};
  int _cntml;
  _nrn_mechanism_cache_range _lmr{_sorted_token, *_nt, *_ml_arg, _type};
  _ml = &_lmr;
  _cntml = _ml_arg->_nodecount;
  Datum *_thread{_ml_arg->_thread};
  double* _globals = nullptr;
  if (gind != 0 && _thread != nullptr) { _globals = _thread[_gth].get<double*>(); }
  for (_iml = 0; _iml < _cntml; ++_iml) {
    _ppvar = _ml_arg->_pdata[_iml];
    _nd = _ml_arg->_nodelist[_iml];
    v = NODEV(_nd);
     _ode_spec1 (_threadargs_);
 }}
 
static void _ode_map(Prop* _prop, int _ieq, neuron::container::data_handle<double>* _pv, neuron::container::data_handle<double>* _pvdot, double* _atol, int _type) { 
  Datum* _ppvar;
  _ppvar = _nrn_mechanism_access_dparam(_prop);
  _cvode_ieq = _ieq;
  for (int _i=0; _i < 4; ++_i) {
    _pv[_i] = _nrn_mechanism_get_param_handle(_prop, _slist1[_i]);
    _pvdot[_i] = _nrn_mechanism_get_param_handle(_prop, _dlist1[_i]);
    _cvode_abstol(_atollist, _atol, _i);
  }
 }
 
static void _ode_matsol_instance1(_internalthreadargsproto_) {
 _ode_matsol1 (_threadargs_);
 }
 
static void _ode_matsol(_nrn_model_sorted_token const& _sorted_token, NrnThread* _nt, Memb_list* _ml_arg, int _type) {
   Datum* _ppvar;
   size_t _iml;   _nrn_mechanism_cache_range* _ml;   Node* _nd{};
  double _v{};
  int _cntml;
  _nrn_mechanism_cache_range _lmr{_sorted_token, *_nt, *_ml_arg, _type};
  _ml = &_lmr;
  _cntml = _ml_arg->_nodecount;
  Datum *_thread{_ml_arg->_thread};
  double* _globals = nullptr;
  if (gind != 0 && _thread != nullptr) { _globals = _thread[_gth].get<double*>(); }
  for (_iml = 0; _iml < _cntml; ++_iml) {
    _ppvar = _ml_arg->_pdata[_iml];
    _nd = _ml_arg->_nodelist[_iml];
    v = NODEV(_nd);
 _ode_matsol_instance1(_threadargs_);
 }}

static void initmodel(_internalthreadargsproto_) {
  int _i; double _save;{
  A2 = A20;
  A1 = A10;
  B2 = B20;
  B1 = B10;
 {
   if ( tau_r_ampa / tau_d_ampa > 0.9999 ) {
     tau_r_ampa = 0.9999 * tau_d_ampa ;
     }
   if ( tau_r_nmda / tau_d_nmda > 0.9999 ) {
     tau_r_nmda = 0.9999 * tau_d_nmda ;
     }
   f_ampa = peaknorm ( _threadargscomma_ tau_r_ampa , tau_d_ampa ) ;
   f_nmda = peaknorm ( _threadargscomma_ tau_r_nmda , tau_d_nmda ) ;
   A1 = 0.0 ;
   A2 = 0.0 ;
   B1 = 0.0 ;
   B2 = 0.0 ;
   nev = 0.0 ;
   }
 
}
}

static void nrn_init(_nrn_model_sorted_token const& _sorted_token, NrnThread* _nt, Memb_list* _ml_arg, int _type){
_nrn_mechanism_cache_range _lmr{_sorted_token, *_nt, *_ml_arg, _type};
auto* const _vec_v = _nt->node_voltage_storage();
auto* const _ml = &_lmr;
Datum* _ppvar; Datum* _thread;
Node *_nd; double _v; int* _ni; int _iml, _cntml;
_ni = _ml_arg->_nodeindices;
_cntml = _ml_arg->_nodecount;
_thread = _ml_arg->_thread;
double* _globals = nullptr;
if (gind != 0 && _thread != nullptr) { _globals = _thread[_gth].get<double*>(); }
for (_iml = 0; _iml < _cntml; ++_iml) {
 _ppvar = _ml_arg->_pdata[_iml];
 _tsav = -1e20;
   _v = _vec_v[_ni[_iml]];
 v = _v;
 initmodel(_threadargs_);
}
}

static double _nrn_current(_internalthreadargsprotocomma_ double _v) {
double _current=0.; v=_v;
{ {
   g_ampa = A2 - A1 ;
   g_nmda = B2 - B1 ;
   mgblock = 1.0 / ( 1.0 + exp ( 0.062 * - v ) * ( mg / 3.57 ) ) ;
   i_ampa = g_ampa * ( v - e ) ;
   i_nmda = g_nmda * mgblock * ( v - e ) ;
   i = i_ampa + i_nmda ;
   }
 _current += i;

} return _current;
}

static void nrn_cur(_nrn_model_sorted_token const& _sorted_token, NrnThread* _nt, Memb_list* _ml_arg, int _type) {
_nrn_mechanism_cache_range _lmr{_sorted_token, *_nt, *_ml_arg, _type};
auto const _vec_rhs = _nt->node_rhs_storage();
auto const _vec_sav_rhs = _nt->node_sav_rhs_storage();
auto const _vec_v = _nt->node_voltage_storage();
auto* const _ml = &_lmr;
Datum* _ppvar; Datum* _thread;
Node *_nd; int* _ni; double _rhs, _v; int _iml, _cntml;
_ni = _ml_arg->_nodeindices;
_cntml = _ml_arg->_nodecount;
_thread = _ml_arg->_thread;
double* _globals = nullptr;
if (gind != 0 && _thread != nullptr) { _globals = _thread[_gth].get<double*>(); }
for (_iml = 0; _iml < _cntml; ++_iml) {
 _ppvar = _ml_arg->_pdata[_iml];
   _v = _vec_v[_ni[_iml]];
 auto const _g_local = _nrn_current(_threadargscomma_ _v + .001);
 	{ _rhs = _nrn_current(_threadargscomma_ _v);
 	}
 _g = (_g_local - _rhs)/.001;
 _g *=  1.e2/(_nd_area);
 _rhs *= 1.e2/(_nd_area);
	 _vec_rhs[_ni[_iml]] -= _rhs;
 
}
 
}

static void nrn_jacob(_nrn_model_sorted_token const& _sorted_token, NrnThread* _nt, Memb_list* _ml_arg, int _type) {
_nrn_mechanism_cache_range _lmr{_sorted_token, *_nt, *_ml_arg, _type};
auto const _vec_d = _nt->node_d_storage();
auto const _vec_sav_d = _nt->node_sav_d_storage();
auto* const _ml = &_lmr;
Datum* _ppvar; Datum* _thread;
Node *_nd; int* _ni; int _iml, _cntml;
_ni = _ml_arg->_nodeindices;
_cntml = _ml_arg->_nodecount;
_thread = _ml_arg->_thread;
double* _globals = nullptr;
if (gind != 0 && _thread != nullptr) { _globals = _thread[_gth].get<double*>(); }
for (_iml = 0; _iml < _cntml; ++_iml) {
  _vec_d[_ni[_iml]] += _g;
 
}
 
}

static void nrn_state(_nrn_model_sorted_token const& _sorted_token, NrnThread* _nt, Memb_list* _ml_arg, int _type) {
_nrn_mechanism_cache_range _lmr{_sorted_token, *_nt, *_ml_arg, _type};
auto* const _vec_v = _nt->node_voltage_storage();
auto* const _ml = &_lmr;
Datum* _ppvar; Datum* _thread;
Node *_nd; double _v = 0.0; int* _ni;
_ni = _ml_arg->_nodeindices;
size_t _cntml = _ml_arg->_nodecount;
_thread = _ml_arg->_thread;
double* _globals = nullptr;
if (gind != 0 && _thread != nullptr) { _globals = _thread[_gth].get<double*>(); }
for (size_t _iml = 0; _iml < _cntml; ++_iml) {
 _ppvar = _ml_arg->_pdata[_iml];
 _nd = _ml_arg->_nodelist[_iml];
   _v = _vec_v[_ni[_iml]];
 v=_v;
{
 {   state(_threadargs_);
  }}}

}

static void terminal(){}

static void _initlists(){
 int _i; static int _first = 1;
  if (!_first) return;
 _slist1[0] = {A1_columnindex, 0};  _dlist1[0] = {DA1_columnindex, 0};
 _slist1[1] = {A2_columnindex, 0};  _dlist1[1] = {DA2_columnindex, 0};
 _slist1[2] = {B1_columnindex, 0};  _dlist1[2] = {DB1_columnindex, 0};
 _slist1[3] = {B2_columnindex, 0};  _dlist1[3] = {DB2_columnindex, 0};
_first = 0;
}

#if NMODL_TEXT
static void register_nmodl_text_and_filename(int mech_type) {
    const char* nmodl_filename = "/home/nishant/lab/project_MFB/MFB_poirazi_model/mfb/mechanisms/mfbsyn.mod";
    const char* nmodl_file_text = 
  "COMMENT\n"
  "MFBSyn: event-driven quantal AMPA + NMDA synapse for vesicle-release input.\n"
  "\n"
  "Written for MFB_poirazi_model (not part of the original Poirazi et al. 2003 model).\n"
  "\n"
  "Every NET_RECEIVE event is one released vesicle. It adds one quantum of AMPA and\n"
  "NMDA conductance (weight = number of vesicles, normally 1). The quanta sum\n"
  "linearly, so k vesicles arriving together give k times the conductance. There is\n"
  "no saturation and no dead time.\n"
  "\n"
  "Each component is a two-exponential (rise/decay) conductance, normalised so that\n"
  "one vesicle gives a peak of exactly gq_ampa (AMPA) and nmda_ratio*gq_ampa (NMDA,\n"
  "before the Mg block):\n"
  "\n"
  "  g_ampa = A2 - A1,   g_nmda = B2 - B1\n"
  "  i_ampa = g_ampa * (v - e)\n"
  "  i_nmda = g_nmda * mgblock(v) * (v - e)\n"
  "  mgblock(v) = 1 / (1 + exp(-0.062 v) * mg / 3.57)      (Jahr & Stevens 1990)\n"
  "\n"
  "Conductances are in uS (NEURON convention for point processes); currents in nA,\n"
  "negative = inward. The Python side sets and reports them in nS / pA.\n"
  "nev counts the vesicles received (for checking event delivery).\n"
  "ENDCOMMENT\n"
  "\n"
  "NEURON {\n"
  "	POINT_PROCESS MFBSyn\n"
  "	RANGE gq_ampa, tau_r_ampa, tau_d_ampa\n"
  "	RANGE nmda_ratio, tau_r_nmda, tau_d_nmda, mg, e\n"
  "	RANGE g_ampa, g_nmda, i_ampa, i_nmda, mgblock, nev\n"
  "	NONSPECIFIC_CURRENT i\n"
  "	THREADSAFE\n"
  "}\n"
  "\n"
  "UNITS {\n"
  "	(nA) = (nanoamp)\n"
  "	(mV) = (millivolt)\n"
  "	(uS) = (microsiemens)\n"
  "	(mM) = (milli/liter)\n"
  "}\n"
  "\n"
  "PARAMETER {\n"
  "	gq_ampa = 0.0005 (uS)    : peak AMPA conductance of one vesicle (0.5 nS)\n"
  "	tau_r_ampa = 0.5 (ms)\n"
  "	tau_d_ampa = 5 (ms)\n"
  "	nmda_ratio = 0.3 (1)     : peak g_NMDA / peak g_AMPA of one vesicle (no Mg block)\n"
  "	tau_r_nmda = 3 (ms)\n"
  "	tau_d_nmda = 70 (ms)\n"
  "	mg = 1 (mM)\n"
  "	e = 0 (mV)\n"
  "}\n"
  "\n"
  "ASSIGNED {\n"
  "	v (mV)\n"
  "	i (nA)\n"
  "	i_ampa (nA)\n"
  "	i_nmda (nA)\n"
  "	g_ampa (uS)\n"
  "	g_nmda (uS)\n"
  "	mgblock (1)\n"
  "	f_ampa (1)\n"
  "	f_nmda (1)\n"
  "	nev (1)\n"
  "}\n"
  "\n"
  "STATE {\n"
  "	A1 (uS)\n"
  "	A2 (uS)\n"
  "	B1 (uS)\n"
  "	B2 (uS)\n"
  "}\n"
  "\n"
  "INITIAL {\n"
  "	if (tau_r_ampa / tau_d_ampa > 0.9999) { tau_r_ampa = 0.9999 * tau_d_ampa }\n"
  "	if (tau_r_nmda / tau_d_nmda > 0.9999) { tau_r_nmda = 0.9999 * tau_d_nmda }\n"
  "	f_ampa = peaknorm(tau_r_ampa, tau_d_ampa)\n"
  "	f_nmda = peaknorm(tau_r_nmda, tau_d_nmda)\n"
  "	A1 = 0\n"
  "	A2 = 0\n"
  "	B1 = 0\n"
  "	B2 = 0\n"
  "	nev = 0\n"
  "}\n"
  "\n"
  "BREAKPOINT {\n"
  "	SOLVE state METHOD cnexp\n"
  "	g_ampa = A2 - A1\n"
  "	g_nmda = B2 - B1\n"
  "	mgblock = 1 / (1 + exp(0.062 (/mV) * -v) * (mg / 3.57 (mM)))\n"
  "	i_ampa = g_ampa * (v - e)\n"
  "	i_nmda = g_nmda * mgblock * (v - e)\n"
  "	i = i_ampa + i_nmda\n"
  "}\n"
  "\n"
  "DERIVATIVE state {\n"
  "	A1' = -A1 / tau_r_ampa\n"
  "	A2' = -A2 / tau_d_ampa\n"
  "	B1' = -B1 / tau_r_nmda\n"
  "	B2' = -B2 / tau_d_nmda\n"
  "}\n"
  "\n"
  "FUNCTION peaknorm(tr (ms), td (ms)) (1) {\n"
  "	LOCAL tp\n"
  "	tp = (tr * td) / (td - tr) * log(td / tr)\n"
  "	peaknorm = 1 / (-exp(-tp / tr) + exp(-tp / td))\n"
  "}\n"
  "\n"
  "NET_RECEIVE(weight (1)) {\n"
  "	A1 = A1 + weight * gq_ampa * f_ampa\n"
  "	A2 = A2 + weight * gq_ampa * f_ampa\n"
  "	B1 = B1 + weight * nmda_ratio * gq_ampa * f_nmda\n"
  "	B2 = B2 + weight * nmda_ratio * gq_ampa * f_nmda\n"
  "	nev = nev + weight\n"
  "}\n"
  ;
    hoc_reg_nmodl_filename(mech_type, nmodl_filename);
    hoc_reg_nmodl_text(mech_type, nmodl_file_text);
}
#endif
