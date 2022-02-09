// Angular
import { Injectable } from '@angular/core';
// RxJS
import {BehaviorSubject, combineLatest, Observable, of} from 'rxjs';

// Object path
import { HttpClient } from '@angular/common/http';
import { select, Store } from '@ngrx/store';
import * as objectPath from 'object-path';
import { map, switchMap } from 'rxjs/operators';
import { environment } from '../../../../../environments/environment';
import { currentUser } from '../../../auth';
import { AppState } from '../../../reducers';
import { IIresults } from '../models/menu-aside.model';
// Services
import { MenuConfigService } from './menu-config.service';

@Injectable()
export class MenuAsideService {
    // Public properties
    menuList$: BehaviorSubject<any[]> = new BehaviorSubject<any[]>([]);

    /**
     * Service constructor
     *
     * @param menuConfigService: MenuConfigService
     */
    constructor(
          private menuConfigService: MenuConfigService,
          private http: HttpClient,
          private store: Store<AppState>,

    ) {
    }

    /**
     * Load menu list
     */
    // loadMenu() {
    //     // get menu list
    //     const menuItems: any[] = objectPath.get(this.menuConfigService.getMenus(), 'aside.items');
    //     this.menuList$.next(menuItems);
    // }

    getUserMenu(): Observable<any[]> {
        return this.store.pipe(select(currentUser),
            switchMap(user => {
                if (user !== undefined) {
                    return this.http.get<IIresults>(environment.apiUrl + '/menu/get')
                    .pipe(
                       map(res => res.results_list),
                    );
                } else {
                return of([]);
                }
            }),
        );
    }
}
