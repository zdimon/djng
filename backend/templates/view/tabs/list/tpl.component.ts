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
	{{class}}Model
} from '../../../store/_models/{{selector}}.tab.model';

import {%class%DataSource} from '../../../store/_data-sources/{{selector}}.tab.datasource';

import {
	{{class}}PageRequested, 
	One{{class}}Deleted,
	Many{{class}}Deleted,
	{{class}}OnServerCreated
} from '../../../store/_actions/{{selector}}.tab.actions';

import {selectLastCreated%class%Id} from '../../../store/_selectors/{{selector}}.tab.selectors';


@Component({
	// tslint:disable-next-line:component-selector
	selector: '{{selector}}',
	templateUrl: './{{selector}}.component.html',
	changeDetection: ChangeDetectionStrategy.OnPush
})
export class {{class}}TabListComponent implements OnInit, OnDestroy {
	// Public properties

	@Input() {{camelName}};
	
	dataSource: {{class}}DataSource;

    displayedColumns = [
		'select',
		{% for i in list_fields %}
		 '{{i.name}}',
		{% endfor %}
		'actions'
		];

	@ViewChild(MatPaginator, {static: true}) paginator: MatPaginator;
	@ViewChild(MatSort, {static: true}) sort: MatSort;
	// Filter fields
	// @ViewChild('searchInput', {static: true}) searchInput: ElementRef;
	// Selection
	selection = new SelectionModel<{{class}}Model>(true, []);
	{{class}}Result: {{class}}Model[] = [];

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
		// 			this.load{{class}}List();
		// 		})
		// 	)
		// 	.subscribe();


		// Init DataSource
		this.dataSource = new {{class}}DataSource(this.store);
		this.dataSource.entitySubject.subscribe(res => this.{{class}}Result = res);

		this.load{{class}}List();

		// this.{{camelName}}$.subscribe(res => {
		// 	if (!res) {
		// 		return;
		// 	}
		// 	this.{{camelName}}$ = res;
        //     this.load{{class}}List();
			
		// });

	}


	/**
	 * Load {{class}} List
	 */
	load{{class}}List() {
		this.selection.clear();
		const queryParams = new QueryParamsModel(
			this.filterConfiguration(),
			// this.sort.direction,
			// this.sort.active,
			// this.paginator.pageIndex,
			// this.paginator.pageSize
		);
		// Call request from server
		this.store.dispatch(new {{class}}PageRequested({
			page: queryParams,
			{{class}}Id: this.{{camelName}}.id
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
    delete{{class}}s() {
        const _title = '{{class}} Delete';
        const _description = 'Are you sure to permanently delete selected {{class}}?';
        const _waitDesciption = '{{class}} are deleting...';
        const _deleteMessage = 'Selected {{class}} have been deleted';

        const dialogRef = this.layoutUtilsService.deleteElement(_title, _description, _waitDesciption);
        dialogRef.afterClosed().subscribe(res => {
            if (!res) {
                return;
            }


			const idsForDeletionSelect =  Object.keys(this.selection.selected).reduce((acc, val) => {
				acc.push(this.selection.selected[val].id);
				return acc;
            }, []);

            this.store.dispatch(new Many{{class}}Deleted({ ids: idsForDeletionSelect }));
            this.layoutUtilsService.showActionNotification(_deleteMessage, MessageType.Delete);
            this.selection.clear();
        });
    }

	/**
     * Check all rows are selected
     */
    isAllSelected() {
        const numSelected = this.selection.selected.length;
        const numRows = this.{{class}}Result.length;
        return numSelected === numRows;
    }

    /**
     * Selects all rows if they are not all selected; otherwise clear selection
     */
    masterToggle() {
        if (this.isAllSelected()) {
            this.selection.clear();
        } else {
            this.{{class}}Result.forEach(row => this.selection.select(row));
        }
    }

}
