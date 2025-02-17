import {
  ChangeDetectorRef,
  Component,
  OnDestroy,
  OnInit,
  ViewEncapsulation
} from '@angular/core';
import * as moment from 'moment';
import {ActivatedRoute} from '@angular/router';
import {untilDestroyed, UntilDestroy} from '@ngneat/until-destroy';
import {PlayersService} from '../_services/players.service';

@UntilDestroy()
@Component({
  selector: 'player-summary-response-component',
  templateUrl: './player-summary-response.component.html',
  styleUrls: ['./player-summary-response.component.scss'],
  encapsulation: ViewEncapsulation.None,
})
export class PlayerSummaryResponseComponent implements OnInit, OnDestroy {

  endpoint: any;
  apiResponse: any;
  playerID: number = 1;

  constructor(
    protected activatedRoute: ActivatedRoute,
    protected cdr: ChangeDetectorRef,
    protected playersService: PlayersService,
  ) {

  }

  ngOnInit(): void {
    this.fetchApiResponse();
  }

  changeParams(): void {
    this.fetchApiResponse();
  }

  fetchApiResponse(): void {
    this.playersService.getPlayerSummary(this.playerID).pipe(untilDestroyed(this)).subscribe(data => {
      this.endpoint = data.endpoint;
      this.apiResponse = JSON.stringify(data.apiResponse, null, 2);
    });
  }

  ngOnDestroy() {
  }

}