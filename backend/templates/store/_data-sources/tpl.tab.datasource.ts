/* ----- {{copyright}} --- */



// RxJS
import { debounceTime } from 'rxjs/operators';
// NGRX
import { Store, select } from '@ngrx/store';
// CRUD
import { BaseDataSource, QueryResultsModel } from '../../../../../core/_base/crud';
// State
import { AppState } from '../../../../../core/reducers';

import { 
	select{{class}}InStore, 
	select{{class}}PageLoading, 
	selectPSShowInitWaitingMessage } 
	from '../_selectors/{{selector}}.tab.selectors';

export class {{class}}DataSource extends BaseDataSource {
	constructor(private store: Store<AppState>) {
		super();

		this.store.pipe(
			select(select{{class}}InStore),
			debounceTime(600)
		).subscribe((response: QueryResultsModel) => {
			this.entitySubject.next(response.items);
			this.paginatorTotalSubject.next(response.totalCount);
		});

		// this.isPreloadTextViewed$ = this.store.pipe(
		// 	select(selectPSShowInitWaitingMessage)
		// );

		this.loading$ = this.store.pipe(select(select{{class}}PageLoading));
	}
}
