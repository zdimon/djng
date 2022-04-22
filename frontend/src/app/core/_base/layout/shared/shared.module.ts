import {Platform} from '@angular/cdk/platform';
import {ModuleWithProviders, NgModule} from '@angular/core';
import {DateAdapter, MAT_DATE_FORMATS} from '@angular/material';
import {MAT_DATE_LOCALE, MatNativeDateModule} from '@angular/material/core';
import {MatDatepickerModule} from '@angular/material/datepicker';
import {MatInputModule} from '@angular/material/input';
import {DateProvider} from '@base/layout';
import {CoreModule} from '@core/core.module';
import { ISO_FORMAT } from './constants';

@NgModule({
	imports: [
		CoreModule,
		MatDatepickerModule,
		MatNativeDateModule,
		MatInputModule,
	],
	exports: [MatDatepickerModule, MatNativeDateModule, MatInputModule],
	declarations: [],
	providers: [
		{
			provide: DateAdapter,
			useClass: DateProvider,
			deps: [MAT_DATE_LOCALE, Platform],
		},
		{
			provide: MAT_DATE_FORMATS,
			useValue: ISO_FORMAT,

		},
	],
})
export class SharedModule {

}
