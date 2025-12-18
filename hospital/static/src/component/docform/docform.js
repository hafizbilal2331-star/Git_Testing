/* @odoo-module */

import { Component, useState, onWillStart } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

export class DocFormView extends Component {
    static template = "hospital.docform";

    static props = {
        record: { optional: true },
        onSave: Function
    };

    setup() {
        this.orm = useService("orm");

        const rec = this.props.record || {};

        this.state = useState({
            id: rec.id || null,
            name: rec.name || "",
            gender: rec.gender || "",
            dob: rec.dob || "",
            address: rec.address || "",
            patients: rec.patients || [],   // 👈 add patients list
        });

        // optional: preload doctors list if you need it
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
            name: this.state.name,
            gender: this.state.gender,
            dob: this.state.dob,
            address: this.state.address,
        };

        if (this.state.id) {
            await this.orm.write("hospital.doctor", [this.state.id], vals);
        } else {
            await this.orm.create("hospital.doctor", [vals]);
        }

        this.props.onSave();
    }
}
