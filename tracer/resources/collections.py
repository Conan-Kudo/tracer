#-*- coding: utf-8 -*-
# collections.py
# Define various kind of collections
#
# Copyright (C) 2014 Jakub Kadlčík
#
# This copyrighted material is made available to anyone wishing to use,
# modify, copy, or redistribute it subject to the terms and conditions of
# the GNU General Public License v.2, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY expressed or implied, including the implied warranties of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
# Public License for more details.  You should have received a copy of the
# GNU General Public License along with this program; if not, write to the
# Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.
#

from __future__ import absolute_import

from operator import attrgetter
from psutil import NoSuchProcess
from tracer.resources.system import System


class ApplicationsCollection(list):

	def sorted(self, attribute):
		return sorted(self, key=attrgetter(attribute))


class ProcessesCollection(list):

	def owned_by(self, user):
		if not user:
			return self
		return self.filtered(lambda process: process.username == user)

	def newer_than(self, timestamp):
		return self.filtered(lambda process: process.create_time >= timestamp)

	def unique(self):
		return ProcessesCollection(set(self))

	def filtered(self, function):
		processes = ProcessesCollection()
		for process in self:
			try:
				if function(process):
					processes.append(process)
			except NoSuchProcess: pass
		return processes


class PackagesCollection(list):

	_package_manager = None

	def __init__(self, *args):
		list.__init__(self, *args)
		self._package_manager = System.package_manager()

	def intersection(self, packages):
		if packages is not None:
			return PackagesCollection(set(packages).intersection(self))
		return self

	@property
	def files(self):
		files = []
		for package in self:
			files.extend(self._package_manager.package_files(package.name))
		return set(files)
