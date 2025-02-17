import {ModuleWithProviders} from '@angular/core';
import {Routes, RouterModule} from '@angular/router';
import {PlayerSummaryResponseComponent} from './player-summary-response.component';


const routes: Routes = [
  { path: '', component: PlayerSummaryResponseComponent, data: { title: 'Player Summary Response'} },
];

export const routing: ModuleWithProviders<RouterModule> = RouterModule.forChild(routes);