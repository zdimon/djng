// Angular
import { Injectable } from '@angular/core';
import { ActivatedRouteSnapshot, CanActivate, Router, RouterStateSnapshot } from '@angular/router';
// NGRX
import { select, Store } from '@ngrx/store';
import { find } from 'lodash';
// RxJS
import { Observable, of } from 'rxjs';
import { map, tap } from 'rxjs/operators';
// Module reducers and selectors
import { AppState} from '../../../core/reducers/';
import { Permission } from '../_models/permission.model';
import { currentUserPermissions } from '../_selectors/auth.selectors';

@Injectable()
export class ModuleGuard implements CanActivate {
    constructor(private store: Store<AppState>, private router: Router) { }

    canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): Observable<boolean>  {

        const moduleName = route.data.moduleName as string;
        if (!moduleName) {
            return of(false);
        }

        return this.store
            .pipe(
                select(currentUserPermissions),
                map((permissions: Permission[]) => {
                    const _perm = find(permissions, (elem: Permission) => {
                        return elem.title.toLocaleLowerCase() === moduleName.toLocaleLowerCase();
                    });
                    return _perm ? true : false;
                }),
                tap(hasAccess => {
                    if (!hasAccess) {
                        this.router.navigateByUrl('/error/403');
                    }
                }),
            );
    }
}
