/* -----  --- */
// Angular
import { Component, OnInit, ChangeDetectionStrategy, OnDestroy, ChangeDetectorRef } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
// Material
import { MatDialog } from '@angular/material';
// RxJS
import { Observable, BehaviorSubject, Subscription, of } from 'rxjs';
import { map, startWith, delay, first } from 'rxjs/operators';
// NGRX
import { Store, select } from '@ngrx/store';
import { Dictionary, Update } from '@ngrx/entity';
import { AppState } from '../../../../../core/reducers';
// Layout
import { SubheaderService } from '../../../../../core/_base/layout';
// CRUD
import { LayoutUtilsService, MessageType, QueryParamsModel } from '../../../../../core/_base/crud';
// Services and Models
import {
	selectLastCreatedPaymentTypeId,
	selectPaymentTypeById,
	PaymentTypeModel,
	PaymentTypeOnServerCreated,
	PaymentTypeUpdated,
	PaymentTypeService
} from '../../store/';

const AVAILABLE_COLORS: string[] =
	['Red', 'CadetBlue', 'Gold', 'LightSlateGrey', 'RoyalBlue', 'Crimson', 'Blue', 'Sienna', 'Indigo', 'Green', 'Violet',
		'GoldenRod', 'OrangeRed', 'Khaki', 'Teal', 'Purple', 'Orange', 'Pink', 'Black', 'DarkTurquoise'];

const AVAILABLE_MANUFACTURES: string[] =
	['Pontiac', 'Subaru', 'Mitsubishi', 'Oldsmobile', 'Chevrolet', 'Chrysler', 'Suzuki', 'GMC', 'Cadillac', 'Mercury', 'Dodge',
		'Ram', 'Lexus', 'Lamborghini', 'Honda', 'Nissan', 'Ford', 'Hyundai', 'Saab', 'Toyota'];

@Component({
	// tslint:disable-next-line:component-selector
	selector: 'kt-paymentType-edit',
	templateUrl: './payment.type-edit.component.html',
	changeDetection: ChangeDetectionStrategy.OnPush,
})
export class PaymentTypeEditComponent implements OnInit, OnDestroy {
	// Public properties
	paymentType: PaymentTypeModel;
	paymentTypeId$: Observable<number>;
	oldPaymentType: PaymentTypeModel;
	selectedTab = 0;
	loadingSubject = new BehaviorSubject<boolean>(true);
	loading$: Observable<boolean>;
	paymentTypeForm: FormGroup;
	hasFormErrors = false;
	filteredColors: Observable<string[]>;
	filteredManufactures: Observable<string[]>;
	// Private password
	private componentSubscriptions: Subscription;
	// sticky portlet header margin
	private headerMargin: number;

	/**
	 * Component constructor
	 *
	 * @param store: Store<AppState>
	 * @param activatedRoute: ActivatedRoute
	 * @param router: Router
	 * @param typesUtilsService: TypesUtilsService
	 * @param paymentTypeFB: FormBuilder
	 * @param dialog: MatDialog
	 * @param subheaderService: SubheaderService
	 * @param layoutUtilsService: SubheaderService
	 * @param layoutConfigService: LayoutConfigService
	 * @param paymentTypeService: PaymentTypesService
	 * @param cdr: ChangeDetectorRef
	 */
	constructor(
		private store: Store<AppState>,
		private activatedRoute: ActivatedRoute,
		private router: Router,
		private paymentTypeFB: FormBuilder,
		public dialog: MatDialog,
		private subheaderService: SubheaderService,
		private layoutUtilsService: LayoutUtilsService,
		private paymentTypeService: PaymentTypeService,
		private cdr: ChangeDetectorRef) {
	}

	/**
	 * @ Lifecycle sequences => https://angular.io/guide/lifecycle-hooks
	 */

	/**
	 * On init
	 */
	ngOnInit() {
		this.loading$ = this.loadingSubject.asObservable();
		this.loadingSubject.next(true);
		this.activatedRoute.params.subscribe(params => {
			const id = params.id;
			if (id && id > 0) {

				this.store.pipe(
					select(selectPaymentTypeById(id))
				).subscribe(result => {
					if (!result) {
						this.loadPaymentTypeFromService(id);
						return;
					}

					this.loadPaymentType(result);
				});
			} else {
				const newPaymentType = new PaymentTypeModel();
				newPaymentType.clear();
				this.loadPaymentType(newPaymentType);
			}
		});

		// sticky portlet header
		window.onload = () => {
			const style = getComputedStyle(document.getElementById('kt_header'));
			this.headerMargin = parseInt(style.height, 0);
		};
	}

	loadPaymentType(_paymentType, fromService: boolean = false) {
		if (!_paymentType) {
			this.goBack('');
		}
		this.paymentType = _paymentType;
		this.paymentTypeId$ = of(_paymentType.id);
		this.oldPaymentType = Object.assign({}, _paymentType);
		this.initPaymentType();
		if (fromService) {
			this.cdr.detectChanges();
		}
	}

	// If product didn't find in store
	loadPaymentTypeFromService(paymentTypeId) {
		this.paymentTypeService.getPaymentTypeById(paymentTypeId).subscribe(res => {
			this.loadPaymentType(res, true);
		});
	}

	/**
	 * On destroy
	 */
	ngOnDestroy() {
		if (this.componentSubscriptions) {
			this.componentSubscriptions.unsubscribe();
		}
	}

	/**
	 * Init product
	 */
	initPaymentType() {
		this.createForm();
		this.loadingSubject.next(false);
		this.subheaderService.setTitle('Edit PaymentType');
	}

	/**
	 * Create form
	 */
	createForm() {
		this.paymentTypeForm = this.paymentTypeFB.group({

			
			
				price: [this.paymentType.price, Validators.required],
		   
				alias: [this.paymentType.alias, Validators.required],
		   
				name: [this.paymentType.name, Validators.required],
		   
				procent_for_agency: [this.paymentType.procent_for_agency, Validators.required],
		   	

			/*
			manufacture: [this.product.manufacture, Validators.required],
			modelYear: [this.product.modelYear.toString(), Validators.required],
			mileage: [this.product.mileage, [Validators.required, Validators.pattern(/^-?(0|[1-9]\d*)?$/)]],
			description: [this.product.description],
			color: [this.product.color, Validators.required],
			price: [this.product.price, [Validators.required, Validators.pattern(/^-?(0|[1-9]\d*)?$/)]],
			condition: [this.product.condition.toString(), [Validators.required, Validators.min(0), Validators.max(1)]],
			status: [this.product.status.toString(), [Validators.required, Validators.min(0), Validators.max(1)]],
			VINCode: [this.product.VINCode, Validators.required]
			*/

		});

		/*
		this.filteredManufactures = this.paymentTypeForm.controls.manufacture.valueChanges
			.pipe(
				startWith(''),
				map(val => this.filterManufacture(val.toString()))
			);
		this.filteredColors = this.productForm.controls.color.valueChanges
			.pipe(
				startWith(''),
				map(val => this.filterColor(val.toString()))
			);
		*/
	}

	/**
	 * Filter manufacture
	 *
	 * @param val: string
	 */

	 /*
	filterManufacture(val: string): string[] {
		return AVAILABLE_MANUFACTURES.filter(option =>
			option.toLowerCase().includes(val.toLowerCase()));
	}
	*/

	/**
	 * Filter color
	 *
	 * @param val: string
	 */
	/*
	filterColor(val: string): string[] {
		return AVAILABLE_COLORS.filter(option =>
			option.toLowerCase().includes(val.toLowerCase()));
	}
	*/
	/**
	 * Go back to the list
	 *
	 * @param id: any
	 */
	goBack(id) {
		this.loadingSubject.next(false);
		const url = `/payment/type/edit?id=${id}`;
		this.router.navigateByUrl(url, { relativeTo: this.activatedRoute });
	}

	goBackWithoutId() {
		this.router.navigateByUrl('/payment/type/list', { relativeTo: this.activatedRoute });
	}

	/**
	 * Refresh product
	 *
	 * @param isNew: boolean
	 * @param id: number
	 */
	refreshPaymentType(isNew: boolean = false, id = 0) {
		this.loadingSubject.next(false);
		let url = this.router.url;
		if (!isNew) {
			this.router.navigate([url], { relativeTo: this.activatedRoute });
			return;
		}

		url = `/ecommerce/products/edit/${id}`;
		this.router.navigateByUrl(url, { relativeTo: this.activatedRoute });
	}

	/**
	 * Reset
	 */
	reset() {
		this.paymentType = Object.assign({}, this.oldPaymentType);
		this.createForm();
		this.hasFormErrors = false;
		this.paymentTypeForm.markAsPristine();
		this.paymentTypeForm.markAsUntouched();
		this.paymentTypeForm.updateValueAndValidity();
	}

	/**
	 * Save data
	 *
	 * @param withBack: boolean
	 */
	onSumbit(withBack: boolean = false) {
		this.hasFormErrors = false;
		const controls = this.paymentTypeForm.controls;
		/** check form */
		if (this.paymentTypeForm.invalid) {
			Object.keys(controls).forEach(controlName =>
				controls[controlName].markAsTouched()
			);

			this.hasFormErrors = true;
			this.selectedTab = 0;
			return;
		}

		// tslint:disable-next-line:prefer-const
		let editedPaymentType = this.preparePaymentType();

		if (editedPaymentType.id > 0) {
			this.updatePaymentType(editedPaymentType, withBack);
			return;
		}

		this.addPaymentType(editedPaymentType, withBack);
	}

	/**
	 * Returns object for saving
	 */
	preparePaymentType(): PaymentTypeModel {
		const controls = this.paymentTypeForm.controls;
		const _paymentType = new PaymentTypeModel();
		_paymentType.id = this.paymentType.id;

		_paymentType.price = controls.price.value;

		_paymentType.alias = controls.alias.value;

		_paymentType.name = controls.name.value;

		_paymentType.procent_for_agency = controls.procent_for_agency.value;
			
		return _paymentType;
	}

	/**
	 * Add product
	 *
	 * @param _paymentType: PaymentTypeModel
	 * @param withBack: boolean
	 */
	addPaymentType(_paymentType: PaymentTypeModel, withBack: boolean = false) {
		this.loadingSubject.next(true);
		this.store.dispatch(new PaymentTypeOnServerCreated({ paymentType: _paymentType }));
		this.componentSubscriptions = this.store.pipe(
			delay(1000),
			select(selectLastCreatedPaymentTypeId)
		).subscribe(newId => {
			if (!newId) {
				return;
			}

			this.loadingSubject.next(false);
			if (withBack) {
				this.goBack(newId);
			} else {
				const message = `New PaymentType successfully has been added.`;
				this.layoutUtilsService.showActionNotification(message, MessageType.Create, 10000, true, true);
				this.refreshPaymentType(true, newId);
			}
		});
	}

	/**
	 * Update product
	 *
	 * @param _paymentType: PaymentTypeModel
	 * @param withBack: boolean
	 */
	updatePaymentType(_paymentType: PaymentTypeModel, withBack: boolean = false) {
		this.loadingSubject.next(true);

		const updatePaymentType: Update<PaymentTypeModel> = {
			id: _paymentType.id,
			changes: _paymentType
		};

		this.store.dispatch(new PaymentTypeUpdated({
			partialPaymentType: updatePaymentType,
			results: _paymentType
		}));

		
			if (withBack) {
				this.goBack(_paymentType.id);
			} else {
				const message = `Item successfully has been saved.`;
				this.layoutUtilsService.showActionNotification(message, MessageType.Update, 10000, true, true);
				this.refreshPaymentType(false);
			}
		
	}

	/**
	 * Returns component title
	 */
	getComponentTitle() {
		let result = 'Create PaymentType';
		if (!this.paymentType || !this.paymentType.id) {
			return result;
		}

		result = `Edit PaymentType`;
		return result;
	}

	/**
	 * Close alert
	 *
	 * @param $event
	 */
	onAlertClose($event) {
		this.hasFormErrors = false;
	}
}
