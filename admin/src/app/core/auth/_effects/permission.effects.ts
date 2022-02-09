// Angular
import { Injectable } from '@angular/core';
// NGRX
import { Actions, Effect, ofType } from '@ngrx/effects';
import { Action } from '@ngrx/store';
import { defer, Observable, of } from 'rxjs';
// RxJS
import { map, mergeMap, tap } from 'rxjs/operators';
// Actions
import {
    AllPermissionsLoaded,
    AllPermissionsRequested,
    PermissionActionTypes,
} from '../_actions/permission.actions';
// Models
import { Permission } from '../_models/permission.model';
// Services
import { AuthService } from '../_services';

@Injectable()
export class PermissionEffects {

    /*
    @Effect()
    loadAllPermissions$ = this.actions$
        .pipe(
            ofType<AllPermissionsRequested>(PermissionActionTypes.AllPermissionsRequested),
            mergeMap(() => this.auth.getAllPermissions()),
            map((result: Permission[]) => {
                return  new AllPermissionsLoaded({
                    permissions: result
                });
            })
          );

    */

    @Effect()
    init$: Observable<Action> = defer(() => {
        return of(new AllPermissionsRequested());
    });

    constructor(private actions$: Actions, private auth: AuthService) { }
}
