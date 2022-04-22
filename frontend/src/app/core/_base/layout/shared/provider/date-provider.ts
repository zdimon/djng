import { Platform } from '@angular/cdk/platform';
import { Injectable } from '@angular/core';
import { NativeDateAdapter } from '@angular/material';
import dayjs from 'dayjs';
import * as customParseFormat from 'dayjs/plugin/customParseFormat';
import * as localizedFormat from 'dayjs/plugin/localizedFormat';

@Injectable()
export class DateProvider extends NativeDateAdapter {
	constructor(matDateLocale: string, platform: Platform) {
		super(matDateLocale, platform);

		// Initalize DayJS-Parser
		dayjs.locale('en');
		dayjs.extend(customParseFormat);
		dayjs.extend(localizedFormat);
	}

	parse(value: any): Date | null {
		return dayjs(value, 'DD-MM-YYYY').toDate();
	}

	format(date: Date, displayFormat: any): string {
		return dayjs(date).format(displayFormat);
	}
}
