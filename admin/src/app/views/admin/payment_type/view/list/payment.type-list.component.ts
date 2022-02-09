/* -----  --- */
// Angular
import { Component, OnInit, ElementRef, ViewChild, ChangeDetectionStrategy, OnDestroy } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
// Material
import { MatPaginator, MatSort, MatDialog } from '@angular/material';
import { SelectionModel } from '@angular/cdk/collections';
// RXJS
import { debounceTime, distinctUntilChanged, tap, skip, delay } from 'rxjs/operators';
import { fromEvent, merge, Observable, of, Subscription } from 'rxjs';
// NGRX
import { Store, select } from '@ngrx/store';
import { AppState } from '@core/reducers';
// UI
import { SubheaderService } from '@core/_base/layout';
// CRUD
import { LayoutUtilsService, MessageType, QueryParamsModel } from '@core/_base/crud';
// Services and Models
import {
    PaymentTypeModel,
    PaymentTypesDataSource,
    PaymentTypesPageRequested,
    OnePaymentTypeDeleted,
    ManyPaymentTypesDeleted,
    PaymentTypesStatusUpdated,
    selectPaymentTypesPageLastQuery
} from '../../store/';

// Table with EDIT item in new page
// ARTICLE for table with sort/filter/paginator
// https://blog.angular-university.io/angular-material-data-table/
// https://v5.material.angular.io/components/table/overview
// https://v5.material.angular.io/components/sort/overview
// https://v5.material.angular.io/components/table/overview#sorting
// https://www.youtube.com/watch?v=NSt9CI3BXv4
@Component({
    // tslint:disable-next-line:component-selector
    selector: 'kt-paymentType-list',
    templateUrl: './payment.type-list.component.html',
    changeDetection: ChangeDetectionStrategy.OnPush
})
export class PaymentTypeListComponent implements OnInit, OnDestroy {
    // Table fields
    dataSource: PaymentTypesDataSource;
    displayedColumns = [
    
    'actions',
    
            'id', 
    
            'name', 
    
            'procent_for_agency', 
    
            'alias', 
    
            'price', 
    
    'actions'
    ];
    @ViewChild(MatPaginator, {static: true}) paginator: MatPaginator;
    @ViewChild('sort1', {static: true}) sort: MatSort;

    // Filter fields
    lastQuery: QueryParamsModel;
    

    //////////
    // Selection
    selection = new SelectionModel<PaymentTypeModel>(true, []);
    productsResult: PaymentTypeModel[] = [];
    private subscriptions: Subscription[] = [];

    /**
     * Component constructor
     *
     * @param dialog: MatDialog
     * @param activatedRoute: ActivatedRoute
     * @param router: Router
     * @param subheaderService: SubheaderService
     * @param layoutUtilsService: LayoutUtilsService
     * @param store: Store<AppState>
     */
    constructor(public dialog: MatDialog,
                   private activatedRoute: ActivatedRoute,
                   private router: Router,
                   private subheaderService: SubheaderService,
                   private layoutUtilsService: LayoutUtilsService,
                   private store: Store<AppState>) { }

    /**
     * @ Lifecycle sequences => https://angular.io/guide/lifecycle-hooks
     */

    /**
     * On init
     */
    ngOnInit() {
        // If the user changes the sort order, reset back to the first page.
        const sortSubscription = this.sort.sortChange.subscribe(() => (this.paginator.pageIndex = 0));
        this.subscriptions.push(sortSubscription);

        /* Data load will be triggered in two cases:
        - when a pagination event occurs => this.paginator.page
        - when a sort event occurs => this.sort.sortChange
        **/
        const paginatorSubscriptions = merge(this.sort.sortChange, this.paginator.page).pipe(
            tap(() => this.loadPaymentTypesList())
        )
        .subscribe();
        this.subscriptions.push(paginatorSubscriptions);

        // Filtration, bind to searchInput
        

        // Set title to page breadCrumbs
        this.subheaderService.setTitle('PaymentType');

        // Init DataSource
        this.dataSource = new PaymentTypesDataSource(this.store);
        const entitiesSubscription = this.dataSource.entitySubject.pipe(
            skip(1),
            distinctUntilChanged()
        ).subscribe(res => {
            this.productsResult = res;
        });
        this.subscriptions.push(entitiesSubscription);
        // const lastQuerySubscription = this.store.pipe(select(selectVideosPageLastQuery)).subscribe(res => this.lastQuery = res);
        // Load last query from store
        //  this.subscriptions.push(lastQuerySubscription);

        // Read from URL itemId, for restore previous state
        const routeSubscription = this.activatedRoute.queryParams.subscribe(params => {
            if (params.id) {
                this.restoreState(this.lastQuery, +params.id);
            }

            // First load
            of(undefined).pipe(delay(1000)).subscribe(() => { // Remove this line, just loading imitation
                this.loadPaymentTypesList();
            }); // Remove this line, just loading imitation
        });
        this.subscriptions.push(routeSubscription);
    }

    /**
     * On Destroy
     */
    ngOnDestroy() {
        this.subscriptions.forEach(el => el.unsubscribe());
    }

    /**
     * Load Products List
     */
    loadPaymentTypesList() {
        this.selection.clear();
        const queryParams = new QueryParamsModel(
            this.filterConfiguration(),
            this.sort.direction,
            this.sort.active,
            this.paginator.pageIndex,
            this.paginator.pageSize
        );
        // Call request from server
        this.store.dispatch(new PaymentTypesPageRequested({ page: queryParams }));
        this.selection.clear();
    }

    /**
     * Returns object for filter
     */
    filterConfiguration(): any {
        const filter: any = {};


        

        return filter;
    }

    /**
     * Change Date picker
     */
    changeDate (name, event) {
        console.log(name);
        console.log(event);
        this.loadPaymentTypesList();
    }

    /**
     * Restore state
     *
     * @param queryParams: QueryParamsModel
     * @param id: number
     */
    restoreState(queryParams: QueryParamsModel, id: number) {

        if (!queryParams.filter) {
            return;
        }







    }

    /** ACTIONS */
    /**
     * Delete product
     *
     * @param _item: ProductModel
     */
    deletePaymentType(_item: PaymentTypeModel) {
        const _title = 'PaymentType Delete';
        const _description = 'Are you sure to permanently delete this PaymentType?';
        const _waitDesciption = 'PaymentType is deleting...';
        const _deleteMessage = `PaymentType has been deleted`;

        const dialogRef = this.layoutUtilsService.deleteElement(_title, _description, _waitDesciption);
        dialogRef.afterClosed().subscribe(res => {
            if (!res) {
                return;
            }

            this.store.dispatch(new OnePaymentTypeDeleted({ id: _item.id }));
            this.layoutUtilsService.showActionNotification(_deleteMessage, MessageType.Delete);
        });
    }

    /**
     * Delete products
     */
    deletePaymentTypes() {
        const _title = 'PaymentType Delete';
        const _description = 'Are you sure to permanently delete selected PaymentType?';
        const _waitDesciption = 'PaymentType are deleting...';
        const _deleteMessage = 'Selected PaymentType have been deleted';

        const dialogRef = this.layoutUtilsService.deleteElement(_title, _description, _waitDesciption);
        dialogRef.afterClosed().subscribe(res => {
            if (!res) {
                return;
            }


			const idsForDeletionSelect =  Object.keys(this.selection.selected).reduce((acc, val) => {
				acc.push(this.selection.selected[val].id);
				return acc;
            }, []);

            this.store.dispatch(new ManyPaymentTypesDeleted({ ids: idsForDeletionSelect }));
            this.layoutUtilsService.showActionNotification(_deleteMessage, MessageType.Delete);
            this.selection.clear();
        });
    }

    /**
     * Fetch selected products
     */


    /**
     * Update status dialog
     */

    /**
     * Redirect to edit page
     *
     * @param id: any
     */
    editPaymentType(id) {
        this.router.navigate(['../edit', id], { relativeTo: this.activatedRoute });
    }

    createPaymentType() {
        this.router.navigateByUrl('/paymentType/add');
    }

    /**
     * Check all rows are selected
     */
    isAllSelected() {
        const numSelected = this.selection.selected.length;
        const numRows = this.productsResult.length;
        return numSelected === numRows;
    }

    /**
     * Selects all rows if they are not all selected; otherwise clear selection
     */
    masterToggle() {
        if (this.isAllSelected()) {
            this.selection.clear();
        } else {
            this.productsResult.forEach(row => this.selection.select(row));
        }
    }

    /* UI */
    /**
     * Returns status string
     *
     * @param status: number
     */
    getItemStatusString(status: number = 0): string {
        switch (status) {
            case 0:
                return 'Selling';
            case 1:
                return 'Sold';
        }
        return '';
    }

    /**
     * Returns CSS Class by status
     *
     * @param status: number
     */
    getItemCssClassByStatus(status: number = 0): string {
        switch (status) {
            case 0:
                return 'success';
            case 1:
                return 'metal';
        }
        return '';
    }

    /**
     * Rerurns condition string
     *
     * @param condition: number
     */
    getItemConditionString(condition: number = 0): string {
        switch (condition) {
            case 0:
                return 'New';
            case 1:
                return 'Used';
        }
        return '';
    }

    /**
     * Returns CSS Class by condition
     *
     * @param condition: number
     */
    getItemCssClassByCondition(condition: number = 0): string {
        switch (condition) {
            case 0:
                return 'accent';
            case 1:
                return 'primary';
        }
        return '';
    }
}
