/*Template,State,Hooks,Services,Lifecycle,Registry*/

/* @odoo-module */

import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { DocFormView } from "@hospital/component/docform/docform";

export class DocListViewAction extends Component {
    static template = "hospital.doclist";
    static components = { DocFormView };

    setup() {
        this.state = useState({
            records: [],
            patientsByDoctor: {},
            showCreateForm: false,
            selectedRecord: null,
        });

        this.orm = useService("orm");
        this.loadRecords();
    }
async loadRecords() {
    const doctors = await this.orm.searchRead(
        "hospital.doctor",
        [],
        ["id","name", "gender", "dob", "address", "patient_ids"]
    );

    const patients = await this.orm.searchRead(
        "hospital.patient",
        [],
        ["name", "doctor_id"]
    );

    const patientsByDoctor = {};
    for (const pat of patients) {
        const docId = pat.doctor_id ? pat.doctor_id[0] : null;
        if (docId) {
            if (!patientsByDoctor[docId]) {
                patientsByDoctor[docId] = 0; // start counter
            }
            patientsByDoctor[docId] += 1; // increment count
        }
    }

    // Format as "x record(s)"
    for (const docId in patientsByDoctor) {
        const count = patientsByDoctor[docId];
        patientsByDoctor[docId] = `${count} record${count > 1 ? 's' : ''}`;
    }

    this.state.records = doctors;
    this.state.patientsByDoctor = patientsByDoctor;
}


    async deleteRecord(recordId) {
        await this.orm.unlink("hospital.doctor", [recordId]);
        await this.loadRecords();
    }

    toggleCreateForm() {
        this.state.showCreateForm = !this.state.showCreateForm;
        if (!this.state.showCreateForm) {
            this.state.selectedRecord = null;
        }
    }

    async editRecord(recordId) {
    const result = await this.orm.read("hospital.doctor", [recordId], [
        "name", "gender", "dob", "address", "patient_ids"
    ]);
    const doctor = result[0];

    // fetch patients of this doctor
    const patients = await this.orm.searchRead(
        "hospital.patient",
        [["doctor_id", "=", recordId]],
        ["id", "name"]
    );

    doctor.patients = patients;   // 👈 attach names

    this.state.selectedRecord = doctor;
    this.state.showCreateForm = true;
}


    async onSave() {
        await this.loadRecords();
        this.state.showCreateForm = false;
        this.state.selectedRecord = null;
    }
}

registry.category("actions").add("hospital.action_doc_list_view", DocListViewAction);
