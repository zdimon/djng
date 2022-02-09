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
	selectLastCreatedPaymentId,
	selectPaymentById,
	PaymentModel,
	PaymentOnServerCreated,
	PaymentUpdated,
	PaymentService
} from '../../store/';

const AVAILABLE_COLORS: string[] =
	['Red', 'CadetBlue', 'Gold', 'LightSlateGrey', 'RoyalBlue', 'Crimson', 'Blue', 'Sienna', 'Indigo', 'Green', 'Violet',
		'GoldenRod', 'OrangeRed', 'Khaki', 'Teal', 'Purple', 'Orange', 'Pink', 'Black', 'DarkTurquoise'];

const AVAILABLE_MANUFACTURES: string[] =
	['Pontiac', 'Subaru', 'Mitsubishi', 'Oldsmobile', 'Chevrolet', 'Chrysler', 'Suzuki', 'GMC', 'Cadillac', 'Mercury', 'Dodge',
		'Ram', 'Lexus', 'Lamborghini', 'Honda', 'Nissan', 'Ford', 'Hyundai', 'Saab', 'Toyota'];

@Component({
	// tslint:disable-next-line:component-selector
	selector: 'kt-payment-edit',
	templateUrl: './payment-edit.component.html',
	changeDetection: ChangeDetectionStrategy.OnPush,
})
export class PaymentEditComponent implements OnInit, OnDestroy {
	// Public properties
	payment: PaymentModel;
	paymentId$: Observable<number>;
	oldPayment: PaymentModel;
	selectedTab = 0;
	loadingSubject = new BehaviorSubject<boolean>(true);
	loading$: Observable<boolean>;
	paymentForm: FormGroup;
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
	 * @param paymentFB: FormBuilder
	 * @param dialog: MatDialog
	 * @param subheaderService: SubheaderService
	 * @param layoutUtilsService: SubheaderService
	 * @param layoutConfigService: LayoutConfigService
	 * @param paymentService: PaymentsService
	 * @param cdr: ChangeDetectorRef
	 */
	constructor(
		private store: Store<AppState>,
		private activatedRoute: ActivatedRoute,
		private router: Router,
		private paymentFB: FormBuilder,
		public dialog: MatDialog,
		private subheaderService: SubheaderService,
		private layoutUtilsService: LayoutUtilsService,
		private paymentService: PaymentService,
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
					select(selectPaymentById(id))
				).subscribe(result => {
					if (!result) {
						this.loadPaymentFromService(id);
						return;
					}

					this.loadPayment(result);
				});
			} else {
				const newPayment = new PaymentModel();
				newPayment.clear();
				this.loadPayment(newPayment);
			}
		});

		// sticky portlet header
		window.onload = () => {
			const style = getComputedStyle(document.getElementById('kt_header'));
			this.headerMargin = parseInt(style.height, 0);
		};
	}

	loadPayment(_payment, fromService: boolean = false) {
		if (!_payment) {
			this.goBack('');
		}
		this.payment = _payment;
		this.paymentId$ = of(_payment.id);
		this.oldPayment = Object.assign({}, _payment);
		this.initPayment();
		if (fromService) {
			this.cdr.detectChanges();
		}
	}

	// If product didn't find in store
	loadPaymentFromService(paymentId) {
		this.paymentService.getPaymentById(paymentId).subscribe(res => {
			this.loadPayment(res, true);
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
	initPayment() {
		this.createForm();
		this.loadingSubject.next(false);
		this.subheaderService.setTitle('Edit Payment');
	}

	/**
	 * Create form
	 */
	createForm() {
		this.paymentForm = this.paymentFB.group({

			
				

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
		this.filteredManufactures = this.paymentForm.controls.manufacture.valueChanges
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
		const url = `/payment/edit?id=${id}`;
		this.router.navigateByUrl(url, { relativeTo: this.activatedRoute });
	}

	goBackWithoutId() {
		this.router.navigateByUrl('/payment/list', { relativeTo: this.activatedRoute });
	}

	/**
	 * Refresh product
	 *
	 * @param isNew: boolean
	 * @param id: number
	 */
	refreshPayment(isNew: boolean = false, id = 0) {
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
		this.payment = Object.assign({}, this.oldPayment);
		this.createForm();
		this.hasFormErrors = false;
		this.paymentForm.markAsPristine();
		this.paymentForm.markAsUntouched();
		this.paymentForm.updateValueAndValidity();
	}

	/**
	 * Save data
	 *
	 * @param withBack: boolean
	 */
	onSumbit(withBack: boolean = false) {
		this.hasFormErrors = false;
		const controls = this.paymentForm.controls;
		/** check form */
		if (this.paymentForm.invalid) {
			Object.keys(controls).forEach(controlName =>
				controls[controlName].markAsTouched()
			);

			this.hasFormErrors = true;
			this.selectedTab = 0;
			return;
		}

		// tslint:disable-next-line:prefer-const
		let editedPayment = this.preparePayment();

		if (editedPayment.id > 0) {
			this.updatePayment(editedPayment, withBack);
			return;
		}

		this.addPayment(editedPayment, withBack);
	}

	/**
	 * Returns object for saving
	 */
	preparePayment(): PaymentModel {
		const controls = this.paymentForm.controls;
		const _payment = new PaymentModel();
		_payment.id = this.payment.id;
			
		return _payment;
	}

	/**
	 * Add product
	 *
	 * @param _payment: PaymentModel
	 * @param withBack: boolean
	 */
	addPayment(_payment: PaymentModel, withBack: boolean = false) {
		this.loadingSubject.next(true);
		this.store.dispatch(new PaymentOnServerCreated({ payment: _payment }));
		this.componentSubscriptions = this.store.pipe(
			delay(1000),
			select(selectLastCreatedPaymentId)
		).subscribe(newId => {
			if (!newId) {
				return;
			}

			this.loadingSubject.next(false);
			if (withBack) {
				this.goBack(newId);
			} else {
				const message = `New Payment successfully has been added.`;
				this.layoutUtilsService.showActionNotification(message, MessageType.Create, 10000, true, true);
				this.refreshPayment(true, newId);
			}
		});
	}

	/**
	 * Update product
	 *
	 * @param _payment: PaymentModel
	 * @param withBack: boolean
	 */
	updatePayment(_payment: PaymentModel, withBack: boolean = false) {
		this.loadingSubject.next(true);

		const updatePayment: Update<PaymentModel> = {
			id: _payment.id,
			changes: _payment
		};

		this.store.dispatch(new PaymentUpdated({
			partialPayment: updatePayment,
			results: _payment
		}));

		
			if (withBack) {
				this.goBack(_payment.id);
			} else {
				const message = `Item successfully has been saved.`;
				this.layoutUtilsService.showActionNotification(message, MessageType.Update, 10000, true, true);
				this.refreshPayment(false);
			}
		
	}

	/**
	 * Returns component title
	 */
	getComponentTitle() {
		let result = 'Create Payment';
		if (!this.payment || !this.payment.id) {
			return result;
		}

		result = `Edit Payment`;
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
