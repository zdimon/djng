import { SessionService } from './../../session.service';

// Angular
import { Injectable } from '@angular/core';
import { NavigationEnd, Router } from '@angular/router';
// NGRX
import { Actions, Effect, ofType } from '@ngrx/effects';
import { Action, select, Store } from '@ngrx/store';
import { defer, Observable, of } from 'rxjs';
// RxJS
import { filter, mergeMap, tap, withLatestFrom } from 'rxjs/operators';
import { environment } from '../../../../environments/environment';
import { AppState } from '../../reducers';
// Auth actions
import { AuthActionTypes, Login, Logout, Register, UserLoaded, UserRequested } from '../_actions/auth.actions';
import { isUserLoaded } from '../_selectors/auth.selectors';
import { AuthService } from '../_services/index';

@Injectable()
export class AuthEffects {

    @Effect({dispatch: false})
    login$ = this.actions$.pipe(
        ofType<Login>(AuthActionTypes.Login),
        tap(action => {
            this.session_service.removeToken();
            this.session_service.setToken(action.payload.authToken);
            // localStorage.setItem(environment.authTokenKey, action.payload.authToken);
            this.store.dispatch(new UserRequested());
        }),
    );

    @Effect({dispatch: false})
    logout$ = this.actions$.pipe(
        ofType<Logout>(AuthActionTypes.Logout),
        tap(() => {
            this.session_service.removeToken();
            localStorage.removeItem(environment.authTokenKey);
            this.router.navigate(['/auth/login'], {queryParams: {returnUrl: this.returnUrl}});
        }),
    );

    @Effect({dispatch: false})
    register$ = this.actions$.pipe(
        ofType<Register>(AuthActionTypes.Register),
        tap(action => {
            localStorage.setItem(environment.authTokenKey, action.payload.authToken);
        }),
    );

    @Effect({dispatch: false})
    loadUser$ = this.actions$
    .pipe(
        ofType<UserRequested>(AuthActionTypes.UserRequested),
        withLatestFrom(this.store.pipe(select(isUserLoaded))),
        filter(([action, _isUserLoaded]) => !_isUserLoaded),
        mergeMap(([action, _isUserLoaded]) => this.auth.getUserByToken()),
        tap(_user => {
            if (_user) {
                this.store.dispatch(new UserLoaded({ user: _user }));
            } else {
                this.store.dispatch(new Logout());
            }
        }),
      );

    @Effect()
    init$: Observable<Action> = defer(() => {
        const userToken = localStorage.getItem(environment.authTokenKey);
        let observableResult = of({type: 'NO_ACTION'});
        if (userToken) {
            observableResult = of(new Login({  authToken: userToken }));
        }
        return observableResult;
    });

    private returnUrl: string;

    constructor(private actions$: Actions,
                private router: Router,
                private auth: AuthService,
                private session_service: SessionService,
                private store: Store<AppState>) {

        this.router.events.subscribe(event => {
            if (event instanceof NavigationEnd) {
                this.returnUrl = event.url;
            }
        });
    }
}
