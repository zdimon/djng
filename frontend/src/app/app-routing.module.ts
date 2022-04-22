// Angular
import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';
// Auth
import {AuthGuard} from './core/auth';
// Components
import {BaseComponent} from './views/theme/base/base.component';
import {ErrorPageComponent} from './views/theme/content/error-page/error-page.component';

const routes: Routes = [
    {path: 'auth', loadChildren: () => import('app/views/pages/auth/auth.module').then(m => m.AuthModule)},

    {
        path: '',
        component: BaseComponent,
        canActivate: [AuthGuard],
        children: [
            {
                path: 'dashboard',
                loadChildren: () => import('app/views/pages/dashboard/dashboard.module').then(m => m.DashboardModule),
            },
            {
                path: 'user',
                loadChildren: () => import('app/views/admin/user/view/user.module').then(m => m.UserModule),
            },
            {
                path: 'error/403',
                component: ErrorPageComponent,
                data: {
                    type: 'error-v6',
                    code: 403,
                    title: '403... Access forbidden',
                    desc: 'Looks like you don\'t have permission to access for requested page.<br> Please, contact administrator',
                },
            },
            {path: 'error/:type', component: ErrorPageComponent},
            {path: '', redirectTo: 'dashboard', pathMatch: 'full'},
            {path: '**', redirectTo: 'dashboard', pathMatch: 'full'},
        ],
    },

    {path: '**', redirectTo: 'error/403', pathMatch: 'full'},
];

@NgModule({
    imports: [
        RouterModule.forRoot(routes),
    ],
    exports: [RouterModule],
})
export class AppRoutingModule {
}
