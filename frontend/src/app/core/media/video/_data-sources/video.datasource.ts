// State
import { select, Store } from '@ngrx/store';
// RxJS
import { delay, distinctUntilChanged } from 'rxjs/operators';
// CRUD
import { BaseDataSource, DjangoQueryResultsModel, QueryResultsModel } from '../../../_base/crud';
import { AppState } from '../../../reducers';
// Selectors
import { selectVideosInStore, selectVideosPageLoading } from '../_selectors/video.selectors';
import { selectVideosInitWaitingMessage } from './../_selectors/video.selectors';

export class VideosDataSource extends BaseDataSource {
    constructor(private store: Store<AppState>) {
        super();
        this.loading$ = this.store.pipe(
            select(selectVideosPageLoading),
        );

        this.isPreloadTextViewed$ = this.store.pipe(
            select(selectVideosInitWaitingMessage),
        );

        this.store.pipe(
            select(selectVideosInStore),
        ).subscribe((response: QueryResultsModel) => {
            this.paginatorTotalSubject.next(response.totalCount);
            this.entitySubject.next(response.items);
        });
    }
}
