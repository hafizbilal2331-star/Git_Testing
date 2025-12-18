/*Template,State,Hooks,Services,Lifecycle,Registry*/

/* @odoo-module */

import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { FormView } from "@hospital/component/formview/formview";

export class ListViewAction extends Component {
    static template = "hospital.listview";
    static components = { FormView };

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
        const result = await this.orm.searchRead("hospital.patient", [], []);
        this.state.records = result;
    }

    async deleteRecord(recordId) {
        await this.orm.unlink("hospital.patient", [recordId]);
        await this.loadRecords();
    }

    toggleCreateForm() {
        this.state.showCreateForm = !this.state.showCreateForm;
        if (!this.state.showCreateForm) {
            this.state.selectedRecord = null;
        }
    }

    async editRecord(recordId) {
        const result = await this.orm.read("hospital.patient", [recordId], [
            "form_no", "name","gender", "dob", "address","doctor_id",
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

registry.category("actions").add("hospital.action_list_view", ListViewAction);
