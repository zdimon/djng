/* ----- Autogenerated by Django! Author: Zharikov Dimitry zdimon77@gmail.com --- */
import { selectPlansInitWaitingMessage } from '../_selectors/plan.selectors';
// RxJS
import { delay, distinctUntilChanged } from 'rxjs/operators';
// CRUD
import { DjangoQueryResultsModel, QueryResultsModel, BaseDataSource } from '@core/_base/crud';
// State
import { Store, select } from '@ngrx/store';
import { AppState } from '../../../../../core/reducers';
// Selectors
import { selectPlansInStore, selectPlansPageLoading } from '../_selectors/plan.selectors';

export class PlansDataSource extends BaseDataSource {
    constructor(private store: Store<AppState>) {
        super();
        this.loading$ = this.store.pipe(
            select(selectPlansPageLoading)
        );

        this.isPreloadTextViewed$ = this.store.pipe(
            select(selectPlansInitWaitingMessage)
        );

        this.store.pipe(
            select(selectPlansInStore)
        ).subscribe((response: QueryResultsModel) => {
            this.paginatorTotalSubject.next(response.totalCount);
            this.entitySubject.next(response.items);
        });
    }
}