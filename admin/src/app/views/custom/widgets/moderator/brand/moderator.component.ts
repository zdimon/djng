// Angular
import { AfterViewInit, Component, OnInit, Input } from '@angular/core';


@Component({
    selector: 'moderator-list-cmp',
    template: '.moderator cmp {{object | json}}',
})
export class ModeratorComponent implements OnInit {
    // Public properties
    
    @Input() object: any;
    ngOnInit(): void {
        
    }

}
