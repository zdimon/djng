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
	selectLastCreatedModerationId,
	selectModerationById,
	ModerationModel,
	ModerationOnServerCreated,
	ModerationUpdated,
	ModerationService
} from '../../store/';

const AVAILABLE_COLORS: string[] =
	['Red', 'CadetBlue', 'Gold', 'LightSlateGrey', 'RoyalBlue', 'Crimson', 'Blue', 'Sienna', 'Indigo', 'Green', 'Violet',
		'GoldenRod', 'OrangeRed', 'Khaki', 'Teal', 'Purple', 'Orange', 'Pink', 'Black', 'DarkTurquoise'];

const AVAILABLE_MANUFACTURES: string[] =
	['Pontiac', 'Subaru', 'Mitsubishi', 'Oldsmobile', 'Chevrolet', 'Chrysler', 'Suzuki', 'GMC', 'Cadillac', 'Mercury', 'Dodge',
		'Ram', 'Lexus', 'Lamborghini', 'Honda', 'Nissan', 'Ford', 'Hyundai', 'Saab', 'Toyota'];

@Component({
	// tslint:disable-next-line:component-selector
	selector: 'kt-moderation-edit',
	templateUrl: './moderation-edit.component.html',
	changeDetection: ChangeDetectionStrategy.OnPush,
})
export class ModerationEditComponent implements OnInit, OnDestroy {
	// Public properties
	moderation: ModerationModel;
	moderationId$: Observable<number>;
	oldModeration: ModerationModel;
	selectedTab = 0;
	loadingSubject = new BehaviorSubject<boolean>(true);
	loading$: Observable<boolean>;
	moderationForm: FormGroup;
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
	 * @param moderationFB: FormBuilder
	 * @param dialog: MatDialog
	 * @param subheaderService: SubheaderService
	 * @param layoutUtilsService: SubheaderService
	 * @param layoutConfigService: LayoutConfigService
	 * @param moderationService: ModerationsService
	 * @param cdr: ChangeDetectorRef
	 */
	constructor(
		private store: Store<AppState>,
		private activatedRoute: ActivatedRoute,
		private router: Router,
		private moderationFB: FormBuilder,
		public dialog: MatDialog,
		private subheaderService: SubheaderService,
		private layoutUtilsService: LayoutUtilsService,
		private moderationService: ModerationService,
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
					select(selectModerationById(id))
				).subscribe(result => {
					if (!result) {
						this.loadModerationFromService(id);
						return;
					}

					this.loadModeration(result);
				});
			} else {
				const newModeration = new ModerationModel();
				newModeration.clear();
				this.loadModeration(newModeration);
			}
		});

		// sticky portlet header
		window.onload = () => {
			const style = getComputedStyle(document.getElementById('kt_header'));
			this.headerMargin = parseInt(style.height, 0);
		};
	}

	loadModeration(_moderation, fromService: boolean = false) {
		if (!_moderation) {
			this.goBack('');
		}
		this.moderation = _moderation;
		this.moderationId$ = of(_moderation.id);
		this.oldModeration = Object.assign({}, _moderation);
		this.initModeration();
		if (fromService) {
			this.cdr.detectChanges();
		}
	}

	// If product didn't find in store
	loadModerationFromService(moderationId) {
		this.moderationService.getModerationById(moderationId).subscribe(res => {
			this.loadModeration(res, true);
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
	initModeration() {
		this.createForm();
		this.loadingSubject.next(false);
		this.subheaderService.setTitle('Edit Moderation');
	}

	/**
	 * Create form
	 */
	createForm() {
		this.moderationForm = this.moderationFB.group({

			
				

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
		this.filteredManufactures = this.moderationForm.controls.manufacture.valueChanges
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
		const url = `/moderation/edit?id=${id}`;
		this.router.navigateByUrl(url, { relativeTo: this.activatedRoute });
	}

	goBackWithoutId() {
		this.router.navigateByUrl('/moderation/list', { relativeTo: this.activatedRoute });
	}

	/**
	 * Refresh product
	 *
	 * @param isNew: boolean
	 * @param id: number
	 */
	refreshModeration(isNew: boolean = false, id = 0) {
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
		this.moderation = Object.assign({}, this.oldModeration);
		this.createForm();
		this.hasFormErrors = false;
		this.moderationForm.markAsPristine();
		this.moderationForm.markAsUntouched();
		this.moderationForm.updateValueAndValidity();
	}

	/**
	 * Save data
	 *
	 * @param withBack: boolean
	 */
	onSumbit(withBack: boolean = false) {
		this.hasFormErrors = false;
		const controls = this.moderationForm.controls;
		/** check form */
		if (this.moderationForm.invalid) {
			Object.keys(controls).forEach(controlName =>
				controls[controlName].markAsTouched()
			);

			this.hasFormErrors = true;
			this.selectedTab = 0;
			return;
		}

		// tslint:disable-next-line:prefer-const
		let editedModeration = this.prepareModeration();

		if (editedModeration.id > 0) {
			this.updateModeration(editedModeration, withBack);
			return;
		}

		this.addModeration(editedModeration, withBack);
	}

	/**
	 * Returns object for saving
	 */
	prepareModeration(): ModerationModel {
		const controls = this.moderationForm.controls;
		const _moderation = new ModerationModel();
		_moderation.id = this.moderation.id;
			
		return _moderation;
	}

	/**
	 * Add product
	 *
	 * @param _moderation: ModerationModel
	 * @param withBack: boolean
	 */
	addModeration(_moderation: ModerationModel, withBack: boolean = false) {
		this.loadingSubject.next(true);
		this.store.dispatch(new ModerationOnServerCreated({ moderation: _moderation }));
		this.componentSubscriptions = this.store.pipe(
			delay(1000),
			select(selectLastCreatedModerationId)
		).subscribe(newId => {
			if (!newId) {
				return;
			}

			this.loadingSubject.next(false);
			if (withBack) {
				this.goBack(newId);
			} else {
				const message = `New Moderation successfully has been added.`;
				this.layoutUtilsService.showActionNotification(message, MessageType.Create, 10000, true, true);
				this.refreshModeration(true, newId);
			}
		});
	}

	/**
	 * Update product
	 *
	 * @param _moderation: ModerationModel
	 * @param withBack: boolean
	 */
	updateModeration(_moderation: ModerationModel, withBack: boolean = false) {
		this.loadingSubject.next(true);

		const updateModeration: Update<ModerationModel> = {
			id: _moderation.id,
			changes: _moderation
		};

		this.store.dispatch(new ModerationUpdated({
			partialModeration: updateModeration,
			results: _moderation
		}));

		
			if (withBack) {
				this.goBack(_moderation.id);
			} else {
				const message = `Item successfully has been saved.`;
				this.layoutUtilsService.showActionNotification(message, MessageType.Update, 10000, true, true);
				this.refreshModeration(false);
			}
		
	}

	/**
	 * Returns component title
	 */
	getComponentTitle() {
		let result = 'Create Moderation';
		if (!this.moderation || !this.moderation.id) {
			return result;
		}

		result = `Edit Moderation`;
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
