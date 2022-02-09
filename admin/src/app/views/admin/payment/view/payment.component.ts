/* -----  --- */
// Angular
import { Component, OnInit, ChangeDetectionStrategy } from '@angular/core';

@Component({
    templateUrl: './payment.component.html',
    changeDetection: ChangeDetectionStrategy.OnPush
})
export class PaymentComponent implements OnInit {
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
