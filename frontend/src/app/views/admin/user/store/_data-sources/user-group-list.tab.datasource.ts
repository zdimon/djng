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
	selectUserGroupInStore, 
	selectUserGroupPageLoading, 
	selectPSShowInitWaitingMessage } 
	from '../_selectors/user-group-list.tab.selectors';

export class UserGroupDataSource extends BaseDataSource {
	constructor(private store: Store<AppState>) {
		super();

		this.store.pipe(
			select(selectUserGroupInStore),
			debounceTime(600)
		).subscribe((response: QueryResultsModel) => {
			this.entitySubject.next(response.items);
			this.paginatorTotalSubject.next(response.totalCount);
		});

		// this.isPreloadTextViewed$ = this.store.pipe(
		// 	select(selectPSShowInitWaitingMessage)
		// );

		this.loading$ = this.store.pipe(select(selectUserGroupPageLoading));
	}
}