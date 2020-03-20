import sys
from PyQt5.QtCore import QObject
from views.query_view import QueryView
from services.querying_service import Querying
from views.stage_progress_view import StageProgressPlot
from views.retrieve_progress_view import RetrieveProgressPlot
from parsers._configparser import getConfigs


class RunController(QObject):
    def __init__(self, _ui):
        super().__init__()
        self.query_view = QueryView()
        self._ui = _ui
        self.config_file = "config.cfg"
        self.query_done = False
        self.SASidsTarget = [int(id) for id in getConfigs("Data", "targetSASids", self.config_file).replace(" ", "").split(",")]
        project = getConfigs("Data", "PROJECTid", self.config_file)

        if len(getConfigs("Data", "calibratorSASids", self.config_file)) == 0:
            if project == "MSSS_HBA_2013":
                self.SASidsCalibrator = [id - 1 for id in self.SASidsTarget]

            else:
                raise Exception("SAS id for calibrator is not set in config.cfg file")
                sys.exit(1)
        else:
            self.SASidsCalibrator = [int(id) for id in getConfigs("Data", "calibratorSASids", self.config_file).replace(" ", "").split(",")]

        self.q1, self.q2 = self.__query()

    def query_progress(self):
        self.show_querying_results()

    def __query(self):
        if getConfigs("Operations", "which_obj",  self.config_file) == "calibrators":
            q1 = Querying(self.SASidsCalibrator, True, self.config_file)
            q2 = None
        elif getConfigs("Operations", "which_obj",  self.config_file) == "target":
            q1 = None
            q2 = Querying(self.SASidsTarget, False, self.config_file)
        else:
            q1 = Querying(self.SASidsCalibrator, True, self.config_file)
            q2 = Querying(self.SASidsTarget, False, self.config_file)
        return q1, q2

    def show_querying_results(self):
        querying_setup = True
        querying_setup2 = True

        while querying_setup:
            self.query_view.show()
            querying_setup = False
        else:
            if not self.query_done:
                while querying_setup2:
                    self.query_station_count()
                    querying_setup2 = False
                else:
                    self.query_data_products()

            self.query_done = True

    def query_station_count(self,):
        if self.q1 is None:
            msg = self.q2.get_station_count()
            self.query_view._ui.querying_message.setText(msg)
        elif self.q2 is None:
            msg = self.q1.get_station_count()
            self.query_view._ui.querying_message.setText(msg)
        else:
            msg1 = self.q1.get_station_count()
            self.query_view._ui.querying_message.setText(msg1)

            msg2 = self.q2.get_station_count()
            self.query_view._ui.querying_message.setText(self.query_view._ui.querying_message.text() + "\n" + msg2)

    def query_data_products(self):
        if self.q1 is None:
            msg2 = self.q2.get_data_products()
            self.query_view._ui.querying_message.setText(self.query_view._ui.querying_message.text() + "\n" + msg2)

        elif self.q2 is None:
            msg1 = self.q1.get_data_products()
            self.query_view._ui.querying_message.setText(self.query_view._ui.querying_message.text() + "\n" + msg1)

        else:
            msg1 = self.q1.get_data_products()
            self.query_view._ui.querying_message.setText(self.query_view._ui.querying_message.text() + "\n" + msg1)

            msg2 = self.q2.get_data_products()
            self.query_view._ui.querying_message.setText(self.query_view._ui.querying_message.text() + "\n" + msg2)

    def query_data_products2(self):
        if self.q1 is None:
            self.q2.get_data_products()

        elif self.q2 is None:
            self.q1.get_data_products()

        else:
            self.q1.get_data_products()

    def stage_progress(self):
        self.stage_progress_plot = StageProgressPlot(self._ui, self)
        self.stage_progress_plot.show()


    def retrieve_progress(self):
        self.retrieve_progress_plot = RetrieveProgressPlot()
        self.retrieve_progress_plot.show()
