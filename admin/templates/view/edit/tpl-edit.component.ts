/* ----- {{copyright}} --- */
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
	selectLastCreated{{upname}}Id,
	select{{upname}}ById,
	{{upname}}Model,
	{{upname}}OnServerCreated,
	{{upname}}Updated,
	{{upname}}Service
} from '../../store/';

const AVAILABLE_COLORS: string[] =
	['Red', 'CadetBlue', 'Gold', 'LightSlateGrey', 'RoyalBlue', 'Crimson', 'Blue', 'Sienna', 'Indigo', 'Green', 'Violet',
		'GoldenRod', 'OrangeRed', 'Khaki', 'Teal', 'Purple', 'Orange', 'Pink', 'Black', 'DarkTurquoise'];

const AVAILABLE_MANUFACTURES: string[] =
	['Pontiac', 'Subaru', 'Mitsubishi', 'Oldsmobile', 'Chevrolet', 'Chrysler', 'Suzuki', 'GMC', 'Cadillac', 'Mercury', 'Dodge',
		'Ram', 'Lexus', 'Lamborghini', 'Honda', 'Nissan', 'Ford', 'Hyundai', 'Saab', 'Toyota'];

@Component({
	// tslint:disable-next-line:component-selector
	selector: 'kt-{{camelName}}-edit',
	templateUrl: './{{fileprefix}}-edit.component.html',
	changeDetection: ChangeDetectionStrategy.OnPush,
})
export class {{upname}}EditComponent implements OnInit, OnDestroy {
	// Public properties
	{{camelName}}: {{upname}}Model;
	{{camelName}}Id$: Observable<number>;
	old{{upname}}: {{upname}}Model;
	selectedTab = 0;
	loadingSubject = new BehaviorSubject<boolean>(true);
	loading$: Observable<boolean>;
	{{camelName}}Form: FormGroup;
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
	 * @param {{camelName}}FB: FormBuilder
	 * @param dialog: MatDialog
	 * @param subheaderService: SubheaderService
	 * @param layoutUtilsService: SubheaderService
	 * @param layoutConfigService: LayoutConfigService
	 * @param {{camelName}}Service: {{upname}}sService
	 * @param cdr: ChangeDetectorRef
	 */
	constructor(
		private store: Store<AppState>,
		private activatedRoute: ActivatedRoute,
		private router: Router,
		private {{camelName}}FB: FormBuilder,
		public dialog: MatDialog,
		private subheaderService: SubheaderService,
		private layoutUtilsService: LayoutUtilsService,
		private {{camelName}}Service: {{upname}}Service,
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
					select(select{{upname}}ById(id))
				).subscribe(result => {
					if (!result) {
						this.load{{upname}}FromService(id);
						return;
					}

					this.load{{upname}}(result);
				});
			} else {
				const new{{upname}} = new {{upname}}Model();
				new{{upname}}.clear();
				this.load{{upname}}(new{{upname}});
			}
		});

		// sticky portlet header
		window.onload = () => {
			const style = getComputedStyle(document.getElementById('kt_header'));
			this.headerMargin = parseInt(style.height, 0);
		};
	}

	load{{upname}}(_{{camelName}}, fromService: boolean = false) {
		if (!_{{camelName}}) {
			this.goBack('');
		}
		this.{{camelName}} = _{{camelName}};
		this.{{camelName}}Id$ = of(_{{camelName}}.id);
		this.old{{upname}} = Object.assign({}, _{{camelName}});
		this.init{{upname}}();
		if (fromService) {
			this.cdr.detectChanges();
		}
	}

	// If product didn't find in store
	load{{upname}}FromService({{camelName}}Id) {
		this.{{camelName}}Service.get{{upname}}ById({{camelName}}Id).subscribe(res => {
			this.load{{upname}}(res, true);
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
	init{{upname}}() {
		this.createForm();
		this.loadingSubject.next(false);
		this.subheaderService.setTitle('Edit {{upname}}');
	}

	/**
	 * Create form
	 */
	createForm() {
		this.{{camelName}}Form = this.{{camelName}}FB.group({

			
			{% for it in edit_fields %}
				{{it.name}}: [this.{{camelName}}.{{it.name}}, Validators.required],
		   {% endfor %}	

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
		this.filteredManufactures = this.{{camelName}}Form.controls.manufacture.valueChanges
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
		const url = `/{{rout}}/edit?id=${id}`;
		this.router.navigateByUrl(url, { relativeTo: this.activatedRoute });
	}

	goBackWithoutId() {
		this.router.navigateByUrl('/{{rout}}/list', { relativeTo: this.activatedRoute });
	}

	/**
	 * Refresh product
	 *
	 * @param isNew: boolean
	 * @param id: number
	 */
	refresh{{upname}}(isNew: boolean = false, id = 0) {
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
		this.{{camelName}} = Object.assign({}, this.old{{upname}});
		this.createForm();
		this.hasFormErrors = false;
		this.{{camelName}}Form.markAsPristine();
		this.{{camelName}}Form.markAsUntouched();
		this.{{camelName}}Form.updateValueAndValidity();
	}

	/**
	 * Save data
	 *
	 * @param withBack: boolean
	 */
	onSumbit(withBack: boolean = false) {
		this.hasFormErrors = false;
		const controls = this.{{camelName}}Form.controls;
		/** check form */
		if (this.{{camelName}}Form.invalid) {
			Object.keys(controls).forEach(controlName =>
				controls[controlName].markAsTouched()
			);

			this.hasFormErrors = true;
			this.selectedTab = 0;
			return;
		}

		// tslint:disable-next-line:prefer-const
		let edited{{upname}} = this.prepare{{upname}}();

		if (edited{{upname}}.id > 0) {
			this.update{{upname}}(edited{{upname}}, withBack);
			return;
		}

		this.add{{upname}}(edited{{upname}}, withBack);
	}

	/**
	 * Returns object for saving
	 */
	prepare{{upname}}(): {{upname}}Model {
		const controls = this.{{camelName}}Form.controls;
		const _{{camelName}} = new {{upname}}Model();
		_{{camelName}}.id = this.{{camelName}}.id;
{% for it in edit_fields %}
		_{{camelName}}.{{it.name}} = controls.{{it.name}}.value;
{% endfor %}			
		return _{{camelName}};
	}

	/**
	 * Add product
	 *
	 * @param _{{camelName}}: {{upname}}Model
	 * @param withBack: boolean
	 */
	add{{upname}}(_{{camelName}}: {{upname}}Model, withBack: boolean = false) {
		this.loadingSubject.next(true);
		this.store.dispatch(new {{upname}}OnServerCreated({ {{camelName}}: _{{camelName}} }));
		this.componentSubscriptions = this.store.pipe(
			delay(1000),
			select(selectLastCreated{{upname}}Id)
		).subscribe(newId => {
			if (!newId) {
				return;
			}

			this.loadingSubject.next(false);
			if (withBack) {
				this.goBack(newId);
			} else {
				const message = `New {{upname}} successfully has been added.`;
				this.layoutUtilsService.showActionNotification(message, MessageType.Create, 10000, true, true);
				this.refresh{{upname}}(true, newId);
			}
		});
	}

	/**
	 * Update product
	 *
	 * @param _{{camelName}}: {{upname}}Model
	 * @param withBack: boolean
	 */
	update{{upname}}(_{{camelName}}: {{upname}}Model, withBack: boolean = false) {
		this.loadingSubject.next(true);

		const update{{upname}}: Update<{{upname}}Model> = {
			id: _{{camelName}}.id,
			changes: _{{camelName}}
		};

		this.store.dispatch(new {{upname}}Updated({
			partial{{upname}}: update{{upname}},
			results: _{{camelName}}
		}));

		
			if (withBack) {
				this.goBack(_{{camelName}}.id);
			} else {
				const message = `Item successfully has been saved.`;
				this.layoutUtilsService.showActionNotification(message, MessageType.Update, 10000, true, true);
				this.refresh{{upname}}(false);
			}
		
	}

	/**
	 * Returns component title
	 */
	getComponentTitle() {
		let result = 'Create {{upname}}';
		if (!this.{{camelName}} || !this.{{camelName}}.id) {
			return result;
		}

		result = `Edit {{upname}}`;
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
