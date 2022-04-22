/* ----- {{copyright}} --- */
import { select{{upname}}sInitWaitingMessage } from '../_selectors/{{fileprefix}}.selectors';
// RxJS
import { delay, distinctUntilChanged } from 'rxjs/operators';
// CRUD
import { DjangoQueryResultsModel, QueryResultsModel, BaseDataSource } from '@core/_base/crud';
// State
import { Store, select } from '@ngrx/store';
import { AppState } from '../../../../../core/reducers';
// Selectors
import { select{{upname}}sInStore, select{{upname}}sPageLoading } from '../_selectors/{{fileprefix}}.selectors';

export class {{upname}}sDataSource extends BaseDataSource {
    constructor(private store: Store<AppState>) {
        super();
        this.loading$ = this.store.pipe(
            select(select{{upname}}sPageLoading)
        );

        this.isPreloadTextViewed$ = this.store.pipe(
            select(select{{upname}}sInitWaitingMessage)
        );

        this.store.pipe(
            select(select{{upname}}sInStore)
        ).subscribe((response: QueryResultsModel) => {
            this.paginatorTotalSubject.next(response.totalCount);
            this.entitySubject.next(response.items);
        });
    }
}
