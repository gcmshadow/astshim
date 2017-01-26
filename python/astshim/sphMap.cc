/*
 * LSST Data Management System
 *
 * This product includes software developed by the
 * LSST Project (http://www.lsst.org/).
 * See the COPYRIGHT file
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the LSST License Statement and
 * the GNU General Public License along with this program.  If not,
 * see <https://www.lsstcorp.org/LegalNotices/>.
 */
#include <memory>

#include <pybind11/pybind11.h>

#include "astshim/Mapping.h"
#include "astshim/SphMap.h"

namespace py = pybind11;
using namespace pybind11::literals;

namespace ast {

PYBIND11_PLUGIN(_sphMap) {
    py::module mod("_sphMap", "Python wrapper for SphMap");

    py::class_<SphMap, std::shared_ptr<SphMap>, Mapping> cls(mod, "SphMap");

    cls.def(py::init<std::string const &>(), "options"_a="");

    cls.def("copy", &SphMap::copy);
    cls.def("getUnitRadius", &SphMap::getUnitRadius);
    cls.def("getPolarLong", &SphMap::getPolarLong);

    return mod.ptr();
}

}  // ast
