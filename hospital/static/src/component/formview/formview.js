/* @odoo-module */

import { Component, useState, onWillStart } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

export class FormView extends Component {
    static template = "hospital.formview";

    static props = {
        record: { optional: true },
        onSave: Function
    };

    setup() {
        this.orm = useService("orm");

        const rec = this.props.record || {};

        this.state = useState({
            form_no: rec.form_no || "",
            name: rec.name || "",
            age: rec.age || "",
            gender: rec.gender || "",
            dob: rec.dob || "",
            address: rec.address || "",
            doctor_id: rec.doctor_id ? rec.doctor_id[0] : null,
            doctors: [],
            id: rec.id || null,
        });


        onWillStart(async () => {
            this.state.doctors = await this.orm.searchRead(
                "hospital.doctor",
                [],
                ["name"]
            );
        });
    }

         async saveRecord() {
             const vals = {
                form_no: this.state.form_no,
                name: this.state.name,
                age: this.state.age,
                gender: this.state.gender,
                dob: this.state.dob,
                address: this.state.address,
                doctor_id: this.state.doctor_id ? Number(this.state.doctor_id) : false,
     };

             if (this.state.id) {
                await this.orm.write("hospital.patient", [this.state.id], vals);
             }
             else {
                await this.orm.create("hospital.patient", [vals]);
             }

    this.props.onSave();
};

}
