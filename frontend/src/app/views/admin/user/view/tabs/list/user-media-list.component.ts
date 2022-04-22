import { Pipe } from '@angular/core';
// Angular
import { Component, OnInit, ElementRef, ViewChild, Input, ChangeDetectionStrategy, OnDestroy } from '@angular/core';
// Material
import { MatPaginator, MatSort, MatDialog } from '@angular/material';
import { SelectionModel } from '@angular/cdk/collections';
// RXJS
import { debounceTime, distinctUntilChanged, tap, delay } from 'rxjs/operators';
import { fromEvent, merge, BehaviorSubject, Subscription, Observable, of } from 'rxjs';
// NGRX
import { Store, select } from '@ngrx/store';
import { Update } from '@ngrx/entity';
import { AppState } from '../../../../../../core/reducers';

// CRUD
import { QueryParamsModel, LayoutUtilsService, MessageType } from '../../../../../../core/_base/crud';


// Services and models
import {
	UserMediaModel
} from '../../../store/_models/user-media-list.tab.model';

import {UserMediaDataSource} from '../../../store/_data-sources/user-media-list.tab.datasource';

import {
	UserMediaPageRequested, 
	OneUserMediaDeleted,
	ManyUserMediaDeleted,
	UserMediaOnServerCreated
} from '../../../store/_actions/user-media-list.tab.actions';

import {selectLastCreatedUserMediaId} from '../../../store/_selectors/user-media-list.tab.selectors';


@Component({
	// tslint:disable-next-line:component-selector
	selector: 'user-media-list',
	templateUrl: './user-media-list.component.html',
	changeDetection: ChangeDetectionStrategy.OnPush
})
export class UserMediaTabListComponent implements OnInit, OnDestroy {
	// Public properties

	@Input() user;
	
	dataSource: UserMediaDataSource;

    displayedColumns = [
		'select',
		
		 'get_small_url_square',
		
		 'role_media',
		
		'actions'
		];

	@ViewChild(MatPaginator, {static: true}) paginator: MatPaginator;
	@ViewChild(MatSort, {static: true}) sort: MatSort;
	// Filter fields
	// @ViewChild('searchInput', {static: true}) searchInput: ElementRef;
	// Selection
	selection = new SelectionModel<UserMediaModel>(true, []);
	UserMediaResult: UserMediaModel[] = [];

	// Private properties
	private componentSubscriptions: Subscription;

	/**
     * Component constructor
     *
     * @param layoutUtilsService: LayoutUtilsService
     */
	constructor(private store: Store<AppState>,
		public dialog: MatDialog, private layoutUtilsService: LayoutUtilsService,) { }

	ngOnInit() {
		// If the user changes the sort order, reset back to the first page.
		// this.sort.sortChange.subscribe(() => (this.paginator.pageIndex = 0));

		/* Data load will be triggered in two cases:
		- when a pagination event occurs => this.paginator.page
		- when a sort event occurs => this.sort.sortChange
		**/
		// merge(this.sort.sortChange, this.paginator.page)
		// 	.pipe(
		// 		tap(() => {
		// 			this.loadUserMediaList();
		// 		})
		// 	)
		// 	.subscribe();


		// Init DataSource
		this.dataSource = new UserMediaDataSource(this.store);
		this.dataSource.entitySubject.subscribe(res => this.UserMediaResult = res);

		this.loadUserMediaList();

		// this.user$.subscribe(res => {
		// 	if (!res) {
		// 		return;
		// 	}
		// 	this.user$ = res;
        //     this.loadUserMediaList();
			
		// });

	}


	/**
	 * Load UserMedia List
	 */
	loadUserMediaList() {
		this.selection.clear();
		const queryParams = new QueryParamsModel(
			this.filterConfiguration(),
			// this.sort.direction,
			// this.sort.active,
			// this.paginator.pageIndex,
			// this.paginator.pageSize
		);
		// Call request from server
		this.store.dispatch(new UserMediaPageRequested({
			page: queryParams,
			UserMediaId: this.user.id
		}));
	}



	/**
	 * Retirns object for filter
	 */
	filterConfiguration(): any {
		const filter: any = {};
		// const searchText: string = this.searchInput.nativeElement.value;

		// filter._specificationName = searchText;
		// filter.value = searchText;
		return filter;
	}

	ngOnDestroy(): void {
		//Called once, before the instance is destroyed.
		//Add 'implements OnDestroy' to the class.
		
	}

	/**
     * Delete products
     */
    deleteUserMedias() {
        const _title = 'UserMedia Delete';
        const _description = 'Are you sure to permanently delete selected UserMedia?';
        const _waitDesciption = 'UserMedia are deleting...';
        const _deleteMessage = 'Selected UserMedia have been deleted';

        const dialogRef = this.layoutUtilsService.deleteElement(_title, _description, _waitDesciption);
        dialogRef.afterClosed().subscribe(res => {
            if (!res) {
                return;
            }


			const idsForDeletionSelect =  Object.keys(this.selection.selected).reduce((acc, val) => {
				acc.push(this.selection.selected[val].id);
				return acc;
            }, []);

            this.store.dispatch(new ManyUserMediaDeleted({ ids: idsForDeletionSelect }));
            this.layoutUtilsService.showActionNotification(_deleteMessage, MessageType.Delete);
            this.selection.clear();
        });
    }

	/**
     * Check all rows are selected
     */
    isAllSelected() {
        const numSelected = this.selection.selected.length;
        const numRows = this.UserMediaResult.length;
        return numSelected === numRows;
    }

    /**
     * Selects all rows if they are not all selected; otherwise clear selection
     */
    masterToggle() {
        if (this.isAllSelected()) {
            this.selection.clear();
        } else {
            this.UserMediaResult.forEach(row => this.selection.select(row));
        }
    }

}
