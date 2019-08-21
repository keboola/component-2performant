import csv
import json
import os
from kbc.result import KBCResult, KBCTableDef

FIELDS_COMMISSIONS = ['id', 'actionid', 'user_id', 'amount', 'status',
                      'affrequest_id', 'description', 'created_at', 'updated_at',
                      'reason', 'transaction_id', 'stats_tags', 'history', 'currency',
                      'working_currency_code', 'program_id', 'registered_in_budget_lock',
                      'from_recruited', 'amount_in_working_currency', 'actiontype', 'user_name',
                      'user_role', 'user_unique_code', 'user_login', 'user_avatar_url',
                      'public_action_data_created_at', 'public_action_data_updated_at',
                      'public_action_data_rate', 'public_action_data_amount', 'public_action_data_ad_type',
                      'public_action_data_ad_id', 'public_action_data_source_ip',
                      'public_action_data_description', 'public_action_data_working_currency_code',
                      'public_action_data_amount_in_working_currency', 'public_click_data_created_at',
                      'public_click_data_source_ip', 'public_click_data_url', 'public_click_data_redirect_to',
                      'public_click_data_device_type']
PK_COMMISSIONS = ['id']


class resultWriter:

    def __init__(self, dataPath, incrementalLoad):

        self.paramDataPath = dataPath
        self.paramIncremental = incrementalLoad
        self.run()

    def createTableDefinition(self, tableName, tableColumns, tablePK):

        _fileName = tableName + '.csv'
        _fullPath = os.path.join(
            self.paramDataPath, 'out', 'tables', _fileName)

        _tableDef = KBCTableDef(
            name=tableName, columns=tableColumns, pk=tablePK)
        _resultDef = KBCResult(file_name=_fileName,
                               full_path=_fullPath, table_def=_tableDef)

        return _resultDef

    @staticmethod
    def createWriter(tableDefinition):

        _writer = csv.DictWriter(open(tableDefinition.full_path, 'w'),
                                 fieldnames=tableDefinition.table_def.columns,
                                 restval='', extrasaction='ignore',
                                 quotechar='"', quoting=csv.QUOTE_ALL)

        _writer.writeheader()

        return _writer

    @staticmethod
    def createManifest(destination, pk=[], incremental=False):

        _manifest = {'primary_key': pk, 'incremental': incremental}

        with open(destination, 'w') as _manFile:

            json.dump(_manifest, _manFile)

    @staticmethod
    def flattenJSON(y):
        out = {}

        def flatten(x, name=''):
            if type(x) is dict:
                for a in x:
                    flatten(x[a], name + a + '_')
            elif type(x) is list:
                i = 0
                for a in x:
                    flatten(a, name + str(i) + '_')
                    i += 1
            else:
                out[name[:-1]] = x

        flatten(y)
        return out

    def run(self):

        _commissionTableDef = self.createTableDefinition(
            'commissions', FIELDS_COMMISSIONS, PK_COMMISSIONS)
        self.writerCommissions = self.createWriter(_commissionTableDef)
        self.createManifest(destination=_commissionTableDef.full_path + '.manifest',
                            pk=_commissionTableDef.table_def.pk,
                            incremental=self.paramIncremental)
