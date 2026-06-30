def display_winner_analysis(df_calc):
    """عرض تحليل الفائز بشكل احترافي"""
    winner = df_calc.loc[df_calc['overall_score'].idxmax()]
    
    st.markdown("---")
    st.markdown("## 🏆 Winner Analysis")
    
    rating = "⭐ A+ (Excellent)" if winner['overall_score'] >= 85 else \
             "⭐ A (Very Good)" if winner['overall_score'] >= 75 else \
             "⭐ B+ (Good)" if winner['overall_score'] >= 65 else \
             "⭐ B (Satisfactory)" if winner['overall_score'] >= 55 else \
             "⭐ C (Needs Improvement)"
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"""
            <div style='background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%); 
                        border-radius: 20px; padding: 30px; border: 3px solid #F59E0B;
                        box-shadow: 0 8px 30px rgba(245,158,11,0.2);'>
                <div style='display: flex; align-items: center; gap: 15px;'>
                    <span style='font-size: 48px;'>🏆</span>
                    <div>
                        <h1 style='color: #92400E; margin: 0; font-size: 32px;'>{winner['company']}</h1>
                        <p style='color: #78350F; margin: 5px 0 0 0; font-size: 16px;'>
                            <strong>🏅 Rank:</strong> #{int(winner['rank'])} | 
                            <strong>📊 ESG Rating:</strong> {rating}
                        </p>
                    </div>
                </div>
                <div style='display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin-top: 20px;'>
                    <div style='background: rgba(255,255,255,0.5); padding: 15px; border-radius: 12px; text-align: center;'>
                        <div style='font-size: 28px; font-weight: 700; color: #2E7D32;'>{winner['environmental_score']:.0f}%</div>
                        <div style='font-size: 13px; color: #78350F;'>🌿 Environmental</div>
                    </div>
                    <div style='background: rgba(255,255,255,0.5); padding: 15px; border-radius: 12px; text-align: center;'>
                        <div style='font-size: 28px; font-weight: 700; color: #1565C0;'>{winner['social_score']:.0f}%</div>
                        <div style='font-size: 13px; color: #78350F;'>👥 Social</div>
                    </div>
                    <div style='background: rgba(255,255,255,0.5); padding: 15px; border-radius: 12px; text-align: center;'>
                        <div style='font-size: 28px; font-weight: 700; color: #6A1B9A;'>{winner['governance_score']:.0f}%</div>
                        <div style='font-size: 13px; color: #78350F;'>🏛️ Governance</div>
                    </div>
                </div>
                <div style='margin-top: 15px; font-size: 14px; color: #78350F;'>
                    <strong>Overall Score:</strong> {winner['overall_score']:.1f}/100
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div style='background: #F8FAFC; border-radius: 20px; padding: 25px; text-align: center; height: 100%; display: flex; flex-direction: column; justify-content: center;'>
                <h3 style='color: #1e293b; margin-top: 0;'>💪 Key Strengths</h3>
                <ul style='list-style: none; padding: 0; margin: 0; text-align: left;'>
                    <li style='padding: 8px 0; border-bottom: 1px solid #e2e8f0;'>✅ GHG Emissions: <strong>{winner['ghg_emissions']:.1f}M t</strong></li>
                    <li style='padding: 8px 0; border-bottom: 1px solid #e2e8f0;'>✅ Methane Intensity: <strong>{winner['methane_intensity']:.2f}%</strong></li>
                    <li style='padding: 8px 0; border-bottom: 1px solid #e2e8f0;'>✅ Recycling Rate: <strong>{winner['recycling_rate']:.1f}%</strong></li>
                    <li style='padding: 8px 0; border-bottom: 1px solid #e2e8f0;'>✅ Safety LTIR: <strong>{winner['safety_ltir']:.3f}</strong></li>
                    <li style='padding: 8px 0;'>✅ R&D Spend: <strong>${winner['rnd_spend']:.0f}M</strong></li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

def display_company_cards(df_calc):
    """عرض بطاقات الشركات بشكل احترافي"""
    st.subheader("📊 Company Rankings")
    df_sorted = df_calc.sort_values('overall_score', ascending=False).reset_index(drop=True)
    
    medal_colors = ['#F59E0B', '#94A3B8', '#CD7F32']
    medal_icons = ['🥇', '🥈', '🥉']
    
    cols = st.columns(len(df_sorted))
    
    for i, (idx, row) in enumerate(df_sorted.iterrows()):
        with cols[i]:
            is_winner = (i == 0)
            border_color = medal_colors[i] if i < 3 else '#475569'
            
            st.markdown(f"""
                <div style='
                    background: white;
                    border-radius: 20px;
                    padding: 25px 20px 20px 20px;
                    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
                    border: 2px solid {border_color};
                    margin: 10px 5px;
                    transition: all 0.3s;
                    text-align: center;
                    height: 100%;
                '>
                    <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;'>
                        <span style='font-size: 28px;'>{medal_icons[i]}</span>
                        {'<span style="background: linear-gradient(135deg, #F59E0B, #D97706); color: white; padding: 4px 16px; border-radius: 30px; font-size: 12px; font-weight: 600; display: inline-block;">🏆 Winner</span>' if is_winner else ''}
                    </div>
                    
                    <h3 style='margin: 10px 0 5px 0; font-size: 20px; color: #1e293b;'>{row['company']}</h3>
                    
                    <div style='font-size: 36px; font-weight: 700; color: {border_color}; margin: 10px 0;'>{row['overall_score']:.1f}</div>
                    <div style='font-size: 14px; color: #64748b; margin-bottom: 15px;'>Overall ESG Score</div>
                    
                    <div style='margin: 15px 0;'>
                        <div style='display: flex; justify-content: space-between; font-size: 13px; color: #334155;'>
                            <span>🌿 Environmental</span>
                            <span style='font-weight: 600;'>{row['environmental_score']:.0f}%</span>
                        </div>
                        <div style='width: 100%; height: 8px; background: #e2e8f0; border-radius: 10px; overflow: hidden; margin: 4px 0 10px 0;'>
                            <div style='width: {min(row['environmental_score'], 100)}%; height: 100%; background: linear-gradient(90deg, #2E7D32, #4CAF50); border-radius: 10px;'></div>
                        </div>
                        
                        <div style='display: flex; justify-content: space-between; font-size: 13px; color: #334155;'>
                            <span>👥 Social</span>
                            <span style='font-weight: 600;'>{row['social_score']:.0f}%</span>
                        </div>
                        <div style='width: 100%; height: 8px; background: #e2e8f0; border-radius: 10px; overflow: hidden; margin: 4px 0 10px 0;'>
                            <div style='width: {min(row['social_score'], 100)}%; height: 100%; background: linear-gradient(90deg, #1565C0, #42A5F5); border-radius: 10px;'></div>
                        </div>
                        
                        <div style='display: flex; justify-content: space-between; font-size: 13px; color: #334155;'>
                            <span>🏛️ Governance</span>
                            <span style='font-weight: 600;'>{row['governance_score']:.0f}%</span>
                        </div>
                        <div style='width: 100%; height: 8px; background: #e2e8f0; border-radius: 10px; overflow: hidden; margin: 4px 0 10px 0;'>
                            <div style='width: {min(row['governance_score'], 100)}%; height: 100%; background: linear-gradient(90deg, #6A1B9A, #AB47BC); border-radius: 10px;'></div>
                        </div>
                    </div>
                    
                    <div style='display: flex; flex-wrap: wrap; gap: 6px; justify-content: center; margin-top: 12px;'>
                        <span style='background: #f1f5f9; padding: 4px 12px; border-radius: 20px; font-size: 12px; color: #334155;'>
                            🌿 GHG: {row['ghg_emissions']:.1f}M
                        </span>
                        <span style='background: #f1f5f9; padding: 4px 12px; border-radius: 20px; font-size: 12px; color: #334155;'>
                            ♻️ Recycle: {row['recycling_rate']:.0f}%
                        </span>
                        <span style='background: #f1f5f9; padding: 4px 12px; border-radius: 20px; font-size: 12px; color: #334155;'>
                            ⚡ Carbon: {row['upstream_carbon_intensity']:.1f}kg
                        </span>
                        <span style='background: #f1f5f9; padding: 4px 12px; border-radius: 20px; font-size: 12px; color: #334155;'>
                            🛡️ Safety: {row['safety_ltir']:.3f}
                        </span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
