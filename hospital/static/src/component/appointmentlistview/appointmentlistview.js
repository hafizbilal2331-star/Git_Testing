/* @odoo-module */

import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { AppointmentFormView } from "@hospital/component/appointmentformview/appointmentformview";

export class AppointmentListViewAction extends Component {
    static template = "hospital.appointmentlistview";
    static components = { AppointmentFormView };

    setup() {
        this.state = useState({
            records: [],
            showCreateForm: false,
            selectedRecord: null,
        });
        this.orm = useService("orm");
        this.loadRecords();
    }

    async loadRecords() {
        const result = await this.orm.searchRead("hospital.appointment", [], []);
        this.state.records = result;
    }

    async deleteRecord(recordId) {
        await this.orm.unlink("hospital.appointment", [recordId]);
        await this.loadRecords();
    }

    toggleCreateForm() {
        this.state.showCreateForm = !this.state.showCreateForm;
        if (!this.state.showCreateForm) {
            this.state.selectedRecord = null;
        }
    }

    async editRecord(recordId) {
        const result = await this.orm.read("hospital.appointment", [recordId], [
            "patient_id", "doctor_id", "date_appointment", "note", "state",
        ]);
        this.state.selectedRecord = result[0];
        this.state.showCreateForm = true;
    }

    async onSave() {
        await this.loadRecords();
        this.state.showCreateForm = false;
        this.state.selectedRecord = null;
    }
}

registry.category("actions").add("hospital.action_appointment_list_view", AppointmentListViewAction);