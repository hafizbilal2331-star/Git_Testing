/* @odoo-module */

import { Component, useState, onWillStart } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

export class AppointmentFormView extends Component {
    static template = "hospital.appointmentformview";

    static props = {
        record: { optional: true },
        onSave: Function
    };

    setup() {
        this.orm = useService("orm");

        const rec = this.props.record || {};

        this.state = useState({
            patient_id: rec.patient_id ? rec.patient_id[0] : null,
            doctor_id: rec.doctor_id ? rec.doctor_id[0] : null,
            date_appointment: rec.date_appointment || "",
            note: rec.note || "",
            state: rec.state || "draft",
            patients: [],
            doctors: [],
            id: rec.id || null,
        });

        onWillStart(async () => {
            this.state.patients = await this.orm.searchRead(
                "hospital.patient",
                [],
                ["name"]
            );
            this.state.doctors = await this.orm.searchRead(
                "hospital.doctor",
                [],
                ["name"]
            );
        });
    }

    async saveRecord() {
        const vals = {
            patient_id: this.state.patient_id ? Number(this.state.patient_id) : false,
            doctor_id: this.state.doctor_id ? Number(this.state.doctor_id) : false,
            date_appointment: this.state.date_appointment,
            note: this.state.note,
            state: this.state.state,
        };

        if (this.state.id) {
            await this.orm.write("hospital.appointment", [this.state.id], vals);
        } else {
            await this.orm.create("hospital.appointment", [vals]);
        }

        this.props.onSave();
    }
}