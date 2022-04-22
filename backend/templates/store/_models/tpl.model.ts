/* ----- {{copyright}} --- */
import { BaseModel } from '@core/_base/crud';


export class {{upname}}Model extends BaseModel {
    {% for i in list_fields %}
        {% if i.type != 'custom' %}
            {{i.name}}: {{i.type}};
        {% endif %}
    {% endfor %}

    clear() {
        {% for i in list_fields %}
            {% if i.type != 'custom' %}
                {% if i.type == 'string' %}
                    this.{{i.name}} = '' ;
                {% endif %}
                {% if i.type == 'number' %}
                    this.{{i.name}} = 0 ;
                {% endif %}
            {% endif %}
         {% endfor %}
    }
}
