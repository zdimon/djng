// State
import { select, Store } from '@ngrx/store';
// RxJS
import { delay, distinctUntilChanged } from 'rxjs/operators';
// CRUD
import { BaseDataSource, QueryResultsModel } from '../../_base/crud';
import { AppState } from '../../reducers';
// Selectors
import { selectProductsInStore, selectProductsPageLoading } from '../_selectors/product.selectors';
import { selectProductsInitWaitingMessage } from './../_selectors/product.selectors';

export class ProductsDataSource extends BaseDataSource {
    constructor(private store: Store<AppState>) {
        super();
        this.loading$ = this.store.pipe(
            select(selectProductsPageLoading),
        );

        this.isPreloadTextViewed$ = this.store.pipe(
            select(selectProductsInitWaitingMessage),
        );

        this.store.pipe(
            select(selectProductsInStore),
        ).subscribe((response: QueryResultsModel) => {
            this.paginatorTotalSubject.next(response.totalCount);
            this.entitySubject.next(response.items);
        });
    }
}
