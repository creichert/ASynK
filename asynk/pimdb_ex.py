##
## Created : Mon Mar 31 15:48:05 IST 2014
##
## Copyright (C) 2014 Sriram Karra <karra.etc@gmail.com>
##
## This file is part of ASynK
##
## ASynK is free software: you can redistribute it and/or modify it under
## the terms of the GNU Affero GPL (GNU AGPL) as published by the
## Free Software Foundation, version 3 of the License
##
## ASynK is distributed in the hope that it will be useful, but WITHOUT
## ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
## FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public
## License for more details.
##
## You should have a copy of the license in the doc/ directory of ASynK.  If
## not, see <http://www.gnu.org/licenses/>.
##
## ####
##
## This is an implementation of the MS Exchange PIMDB by extending the PIMDB
## abstract base class

import logging

from   pyews.ews.data import FolderClass
from   pyews.ews.data       import FolderClass, EWSCreateFolderError
from   pyews.pyews    import WebCredentials, ExchangeService
from   pyews.ews.autodiscover import EWSAutoDiscover, ExchangeAutoDiscoverError
from   folder         import Folder
from   pimdb          import PIMDB

folder_class_map = {
    Folder.CONTACT_t : FolderClass.Contacts,
    Folder.TASK_t    : FolderClass.Tasks,
    Folder.APPT_t    : FolderClass.Calendars,
    Folder.NOTE_t    : FolderClass.Notes
    }

class EXPIMDB(PIMDB):

    def __init__ (self, config, user, pw, url):
        PIMDB.__init__(self, config)
        self.set_user(user)
        self.set_pw(pw)
        self.set_url(url)

        self.ews_init()
        self.set_folders()
        self.set_def_folders()

    ##
    ## First implementation of the abstract methods of PIMDB.
    ##

    def get_dbid (self):
        """See the documentation in class PIMDB"""

        return 'ex'

    def list_folders (self, gid):
        logging.info('%s: Not Implemented', 'pimdb_ex:list_folders()')

    def new_folder (self, fname, ftype=Folder.CONTACT_t, storeid=None):
        """Create a new folder of specified type and return an id. The folder
        will not contain any items. If storeid is None the folder is
        created in the smessage root folder. Otherwise the new folder is
        created in the specified folder.

        type has to be one of the Folder.valid_types
        """

        if not ftype in Folder.valid_types:
            logging.error('Cannot create folder of type: %s', ftype)
            return None

        if not storeid:
            storeid = self.ews.get_root_folder().Id

        try:
            info = [(fname, folder_class_map[ftype])]
            res = self.get_ews().CreateFolder(storeid, info)
        except EWSCreateFolderError as e:
            logging.error('Could not create folder (%s): %s', fname, e)

    def show_folder (self, gid):
        logging.info('%s: Not Implemented', 'pimdb_ex:show_folder()')

    def del_folder (self, gid):
        logging.info('%s: Not Implemented', 'pimdb_ex:del_folder()')

    def set_folders (self):
        """See the documentation in class PIMDB"""

        ## This copies all the folders from the underlying message stores into
        ## the current object for easy referencing
        logging.debug('EXPIMDB.set_folders(): Not implemented')

    def set_def_folders (self):
        """See the documentation in class PIMDB"""

        # self.def_folder['contacts'] = self.folders['contacts'][0]
        pass

    def set_sync_folders (self):
        """See the documentation in class PIMDB"""

        raise NotImplementedError

    def prep_for_sync (self, dbid, pname, dr):
        pass

    ##
    ## Now the non-abstract methods and internal methods
    ##

    def get_user (self):
        return self.user

    def set_user (self, user):
        self.user = user

    def get_pw (self):
        return self.pw

    def set_pw (self, pw):
        self.pw = pw

    def get_url (self):
        return self.url

    def set_url (self, url):
        self.url = url

    def get_ews (self):
        return self.ews

    def set_ews (self, ews):
        self.ews = ews

    def ews_init (self):
        logging.debug('Username: %s; Url: %s', self.user, self.url)

        creds = WebCredentials(self.user, self.pw)
        ews = ExchangeService()
        ews.credentials = creds

        try:
            ews.AutoDiscoverUrl()
        except ExchangeAutoDiscoverError as e:
            logging.info('ExchangeAutoDiscoverError: %s', e)
            logging.info('Falling back on manual url setting.')
            ews.Url = self.url

        ews.init_soap_client()
        self.set_ews(ews)
