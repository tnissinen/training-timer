# test_timer.py
import unittest
from unittest.mock import Mock, patch
import tkinter as tk
from timer_model import TimerModel
from phase_manager import PhaseManager
from timer_controller import TimerController
from timer_view import TimerView

class TestTimerModel(unittest.TestCase):
    def setUp(self):
        self.model = TimerModel()

    def test_initial_state(self):
        self.assertFalse(self.model.running)
        self.assertIsNone(self.model.phase_start_time)
        self.assertIsNone(self.model.total_start_time)
        self.assertEqual(self.model.phase_paused_time, 0)
        self.assertEqual(self.model.total_paused_time, 0)
        self.assertEqual(self.model.current_phase_index, 0)
        self.assertEqual(self.model.current_phase_duration, 0)
        self.assertIsNone(self.model.pause_start_time)

    def test_start(self):
        self.model.start()
        self.assertTrue(self.model.running)
        self.assertIsNotNone(self.model.phase_start_time)
        self.assertIsNotNone(self.model.total_start_time)

    def test_pause(self):
        self.model.start()
        self.model.pause()
        self.assertFalse(self.model.running)
        self.assertIsNotNone(self.model.pause_start_time)

    def test_reset(self):
        self.model.start()
        self.model.reset()
        self.assertFalse(self.model.running)
        self.assertIsNone(self.model.phase_start_time)
        self.assertIsNone(self.model.total_start_time)
        self.assertEqual(self.model.phase_paused_time, 0)
        self.assertEqual(self.model.total_paused_time, 0)
        self.assertEqual(self.model.current_phase_index, 0)
        self.assertEqual(self.model.current_phase_duration, 0)
        self.assertIsNone(self.model.pause_start_time)

    def test_get_elapsed_time(self):
        self.model.start()
        self.assertGreaterEqual(self.model.get_elapsed_time(), 0)

    def test_get_total_elapsed_time(self):
        self.model.start()
        self.assertGreaterEqual(self.model.get_total_elapsed_time(), 0)

class TestPhaseManager(unittest.TestCase):
    def setUp(self):
        self.manager = PhaseManager()

    def test_initial_state(self):
        self.assertEqual(len(self.manager.phases), 0)

    def test_load_phases(self):
        with patch('builtins.open', unittest.mock.mock_open(read_data='[{"name": "Phase 1", "time": "01:00"}]')):
            self.assertTrue(self.manager.load_phases('dummy_path'))
            self.assertEqual(len(self.manager.phases), 1)
            self.assertEqual(self.manager.phases[0], ("Phase 1", "01:00"))

    def test_save_phases(self):
        self.manager.phases = [("Phase 1", "01:00")]
        with patch('builtins.open', unittest.mock.mock_open()) as mock_file:
            self.assertTrue(self.manager.save_phases('dummy_path'))
            mock_file.assert_called_once_with('dummy_path', 'w')

    def test_generate_default_phases(self):
        self.manager.generate_default_phases(2)
        self.assertEqual(len(self.manager.phases), 2)

    def test_get_phase(self):
        self.manager.phases = [("Phase 1", "01:00")]
        self.assertEqual(self.manager.get_phase(0), ("Phase 1", "01:00"))
        self.assertIsNone(self.manager.get_phase(1))

    def test_set_phase(self):
        self.manager.phases = [("Phase 1", "01:00")]
        self.manager.set_phase(0, "Phase 2", "02:00")
        self.assertEqual(self.manager.phases[0], ("Phase 2", "02:00"))

    def test_add_phase(self):
        self.manager.add_phase("Phase 1", "01:00")
        self.assertEqual(len(self.manager.phases), 1)

    def test_remove_phase(self):
        self.manager.phases = [("Phase 1", "01:00")]
        self.manager.remove_phase(0)
        self.assertEqual(len(self.manager.phases), 0)

    def test_get_phase_count(self):
        self.manager.phases = [("Phase 1", "01:00")]
        self.assertEqual(self.manager.get_phase_count(), 1)

class TestTimerController(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.controller = TimerController(self.root)

    def tearDown(self):
        self.root.destroy()

    def test_initial_state(self):
        self.assertIsInstance(self.controller.model, TimerModel)
        self.assertIsInstance(self.controller.phase_manager, PhaseManager)
        self.assertIsInstance(self.controller.view, TimerView)

    def test_toggle_timer(self):
        self.controller.view.num_phases_entry.get = Mock(return_value='2')
        self.controller.generate_phases()
        self.controller.toggle_timer()
        self.assertTrue(self.controller.model.running)
        self.controller.toggle_timer()
        self.assertFalse(self.controller.model.running)

    def test_reset_timer(self):
        self.controller.model.start()
        self.controller.reset_timer()
        self.assertFalse(self.controller.model.running)

    def test_save_phases(self):
        self.controller.view.get_phase_inputs = Mock(return_value=[("Phase 1", "01:00")])
        with patch('tkinter.filedialog.asksaveasfilename', return_value='dummy_path'):
            with patch('timer_controller.messagebox.showinfo'):
                self.controller.save_phases()
                self.assertEqual(len(self.controller.phase_manager.phases), 1)

    def test_generate_phases(self):
        self.controller.view.num_phases_entry.get = Mock(return_value='2')
        self.controller.generate_phases()
        self.assertEqual(len(self.controller.phase_manager.phases), 2)

    def test_toggle_fullscreen(self):
        self.controller.view.master.attributes = Mock(return_value=False)
        self.controller.toggle_fullscreen()
        self.controller.view.master.attributes.assert_called_with('-fullscreen', True)

class TestTimerView(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.view = TimerView(self.root)

    def tearDown(self):
        self.root.destroy()

    def test_initial_state(self):
        self.assertEqual(self.view.master.title(), "Training Timer")

    def test_update_timer_display(self):
        self.view.update_timer_display("01:00", "red")
        self.assertEqual(self.view.timer_label.cget("text"), "01:00")
        self.assertEqual(self.view.timer_label.cget("fg"), "red")

    def test_update_phase_display(self):
        self.view.update_phase_display("Phase 1", "red")
        self.assertEqual(self.view.status_label.cget("text"), "Phase 1")
        self.assertEqual(self.view.status_label.cget("fg"), "red")

    def test_update_total_time_display(self):
        self.view.update_total_time_display("01:00", "02:00", "red")
        self.assertEqual(self.view.total_time_label.cget("text"), "Total Time: 01:00/02:00")
        self.assertEqual(self.view.total_time_label.cget("fg"), "red")

    def test_update_current_phase_total_time(self):
        self.view.update_current_phase_total_time("01:00", "red")
        self.assertEqual(self.view.current_phase_total_time_label.cget("text"), "/01:00")
        self.assertEqual(self.view.current_phase_total_time_label.cget("fg"), "red")

    def test_create_phase_inputs(self):
        self.view.create_phase_inputs(2)
        self.assertEqual(len(self.view.phase_inputs), 2)

    def test_get_phase_inputs(self):
        self.view.create_phase_inputs(2)
        self.view.phase_inputs[0][0].insert(0, "Phase 1")
        self.view.phase_inputs[0][1].insert(0, "01:00")
        self.assertEqual(self.view.get_phase_inputs(), [("Phase 1", "01:00"), ("", "")])

    def test_set_phase_inputs(self):
        self.view.create_phase_inputs(2)
        self.view.set_phase_inputs([("Phase 1", "01:00"), ("Phase 2", "02:00")])
        self.assertEqual(self.view.phase_inputs[0][0].get(), "Phase 1")
        self.assertEqual(self.view.phase_inputs[0][1].get(), "01:00")
        self.assertEqual(self.view.phase_inputs[1][0].get(), "Phase 2")
        self.assertEqual(self.view.phase_inputs[1][1].get(), "02:00")

if __name__ == '__main__':
    unittest.main()