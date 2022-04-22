/* ----- {{copyright}} --- */
import { BaseModel } from '@core/_base/crud';


export class {{class}}Model extends BaseModel {

    id: number;

    {% for i in list_fields %}
        {{i.name}}: {{i.type}};
    {% endfor %}

    clear() {
        this.id = undefined;
        {% for i in list_fields %}
            {% if i.type == 'string' %}
                this.{{i.name}} = '' ;
            {% endif %}
            {% if i.type == 'number' %}
                this.{{i.name}} = 0 ;
            {% endif %}
         {% endfor %}
    }
}
