/* ----- Autogenerated by Django! Author: Zharikov Dimitry zdimon77@gmail.com --- */



// RxJS
import { debounceTime } from 'rxjs/operators';
// NGRX
import { Store, select } from '@ngrx/store';
// CRUD
import { BaseDataSource, QueryResultsModel } from '../../../../../core/_base/crud';
// State
import { AppState } from '../../../../../core/reducers';

import { 
	selectUserMediaInStore, 
	selectUserMediaPageLoading, 
	selectPSShowInitWaitingMessage } 
	from '../_selectors/user-media-list.tab.selectors';

export class UserMediaDataSource extends BaseDataSource {
	constructor(private store: Store<AppState>) {
		super();

		this.store.pipe(
			select(selectUserMediaInStore),
			debounceTime(600)
		).subscribe((response: QueryResultsModel) => {
			this.entitySubject.next(response.items);
			this.paginatorTotalSubject.next(response.totalCount);
		});

		// this.isPreloadTextViewed$ = this.store.pipe(
		// 	select(selectPSShowInitWaitingMessage)
		// );

		this.loading$ = this.store.pipe(select(selectUserMediaPageLoading));
	}
}
