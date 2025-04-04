int cmd_argc = 1;
const char* default_argv = "openroadpy";
char** cmd_argv = const_cast<char**>(&default_argv);

#include <tcl.h>
#define PY_SSIZE_T_CLEAN
#include "Python.h"

#include <array>
#include <clocale>
#include <string>

#include "ord/Design.h"
#include "ord/InitOpenRoad.hh"
#include "ord/OpenRoad.hh"
#include "ord/Tech.h"
#include "sta/StaMain.hh"
#include "sta/StringUtil.hh"
#include "utl/Logger.h"

using std::string;

// Define internal module variables to replace external variables
static const char* internal_prog_name = "openroadpy";
static char** internal_argv = const_cast<char**>(&internal_prog_name);
static int internal_argc = 1;

#define FOREACH_TOOL_WITHOUT_OPENROAD(X) \
  X(ifp)                                 \
  X(utl)                                 \
  X(ant)                                 \
  X(grt)                                 \
  X(gpl)                                 \
  X(dpl)                                 \
  X(ppl)                                 \
  X(tap)                                 \
  X(cts)                                 \
  X(drt)                                 \
  X(dpo)                                 \
  X(fin)                                 \
  X(par)                                 \
  X(rcx)                                 \
  X(rmp)                                 \
  X(stt)                                 \
  X(psm)                                 \
  X(pdn)                                 \
  X(odb)

#define FOREACH_TOOL(X)            \
  FOREACH_TOOL_WITHOUT_OPENROAD(X) \
  X(openroad_swig)

extern "C" {
#define X(name) extern PyObject* PyInit__##name##_py();
FOREACH_TOOL(X)
#undef X
}

namespace sta {
#define X(name) extern const char* name##_py_python_inits[];
FOREACH_TOOL(X)
#undef X
}  // namespace sta

// Add implementation of tclInit function to resolve linking errors
namespace ord {
  int tclInit(Tcl_Interp* interp) {
    // Simple implementation, return success
    return TCL_OK;
  }
  
  // Add implementation of tclAppInit function, which might be needed in some cases
  int tclAppInit(int& argc, char* argv[], const char* init_filename, Tcl_Interp* interp) {
    // Simple implementation, return success
    return TCL_OK;
  }
}  // namespace ord

// Define a simple struct to manage OpenRoad's Tech and Design objects
struct TechAndDesign
{
  std::unique_ptr<ord::Tech> tech;
  std::unique_ptr<ord::Design> design;
};

static TechAndDesign the_tech_and_design;

// Initialize OpenRoad components
static bool initOpenRoadComponents()
{
  // Initialize locale settings to avoid issues with C functions like strtod that depend on locale
  std::array locales = {"en_US.UTF-8", "C.UTF-8", "C"};
  for (auto locale : locales) {
    if (std::setlocale(LC_ALL, locale) != nullptr) {
      setenv("LC_ALL", locale, /* override */ 1);
      break;
    }
  }

  // Create Tcl interpreter and initialize OpenRoad
  auto* interp = Tcl_CreateInterp();
  Tcl_Init(interp);
  
  the_tech_and_design.tech = std::make_unique<ord::Tech>(interp);
  the_tech_and_design.design = std::make_unique<ord::Design>(the_tech_and_design.tech.get());
  ord::OpenRoad::setOpenRoad(the_tech_and_design.design->getOpenRoad());
  
  // Initialize OpenRoad without log and metrics files
  ord::initOpenRoad(interp, nullptr, nullptr);
  
  // Set default thread count
  ord::OpenRoad::openRoad()->setThreadCount(
      ord::OpenRoad::openRoad()->getThreadCount(), false);
  
  return true;
}


// Create an OpenRoad Python module
static PyObject* createOpenRoadModule()
{
  static struct PyModuleDef moduledef = {
      PyModuleDef_HEAD_INIT,
      "openroadpy",                    // Module name
      nullptr,                         // Module documentation
      -1,                              // Size per interpreter state
      nullptr,                         // Method table
      nullptr, nullptr, nullptr, nullptr
  };

  PyObject* module = PyModule_Create(&moduledef);
  if (module == nullptr) {
    return nullptr;
  }

  // Register all tool modules as submodules
#define X(name)                                                             \
  {                                                                         \
    PyObject* submodule = PyInit__##name##_py();                            \
    if (submodule == nullptr) {                                             \
      fprintf(stderr, "Error: Unable to initialize module _" #name "_py\n");              \
      Py_DECREF(module);                                                    \
      return nullptr;                                                       \
    }                                                                       \
    if (PyModule_AddObject(module, "_" #name "_py", submodule) < 0) {       \
      fprintf(stderr, "Error: Unable to add submodule _" #name "_py\n");              \
      Py_DECREF(submodule);                                                 \
      Py_DECREF(module);                                                    \
      return nullptr;                                                       \
    }                                                                       \
  }
  FOREACH_TOOL(X)
#undef X


  
  // Add version information
  // PyModule_AddStringConstant(module, "version", ord::OpenRoad::getVersion());
  // PyModule_AddStringConstant(module, "git_describe", ord::OpenRoad::getGitDescribe());

  return module;
}

// Python module initialization function
PyMODINIT_FUNC
PyInit_openroadpy(void)
{
  // Initialize OpenRoad components
  if (!initOpenRoadComponents()) {
    PyErr_SetString(PyExc_RuntimeError, "Unable to initialize OpenROAD components");
    return nullptr;
  }



  // Create and return the module
  return createOpenRoadModule();
} 