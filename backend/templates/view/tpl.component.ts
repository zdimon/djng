/* ----- {{copyright}} --- */
// Angular
import { Component, OnInit, ChangeDetectionStrategy } from '@angular/core';

@Component({
    templateUrl: './{{fileprefix}}.component.html',
    changeDetection: ChangeDetectionStrategy.OnPush
})
export class {{upname}}Component implements OnInit {
    /**
     * Component constructor
     *
     * @param store: Store<AppState>
     * @param router: Router
     */
    constructor() {}

    /*
     * @ Lifecycle sequences => https://angular.io/guide/lifecycle-hooks
    */

    /**
     * On init
     */
    ngOnInit() {}
}
