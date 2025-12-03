import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

export interface Recommendation {
  isin: string;
  assetname: string;
  assetcategory: string;
  sector: string | null;
  industry: string | null;
  current_price: number;
  profitability: number;
  recommendation_date: string;
}

export interface RecommendationResponse {
  status: string;
  recommendations: Recommendation[];
}

@Injectable({
  providedIn: 'root'
})
export class RecommendationService {
  private apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) { }

  requestRecommendations(customerId: string): Observable<{ status: string }> {
    return this.http.post<{ status: string }>(
      `${this.apiUrl}/recommendations`,
      {
        customer_id: customerId,
        action: 'request_recs'
      }
    );
  }

  getRecommendations(customerId: string): Observable<RecommendationResponse> {
    return this.http.get<RecommendationResponse>(
      `${this.apiUrl}/recommendations/${customerId}`
    );
  }

  logInteraction(customerId: string, isin: string, type: string = 'click'): Observable<{ status: string }> {
    return this.http.post<{ status: string }>(
      `${this.apiUrl}/user_interactions`,
      {
        customer_id: customerId,
        isin: isin,
        type: type
      }
    );
  }
}

