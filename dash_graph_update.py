class upd_gr_dash():
    ##import as ugd - suggestion
    import pandas as pd
    import plotly.graph_objs as go
    import ch1
    import decimal as D

    def __init__(self, *args, **kwargs):

        return super().__init__(*args, **kwargs)
    
    def upd_bar(self, entry_data, sql_stat, name, col):
        import pandas as pd
        import plotly.graph_objs as go
        import ch1
        a = ch1.IntoPostgres(entry_data[0], entry_data[1], entry_data[2], entry_data[3], entry_data[4])
        a.pcur(a.dbase, a.host, a.port, a.usern, a.pw)
        a.pX(sql_stat)
        b = a.cur.fetchall()
        c = pd.DataFrame(b)
        x = c[0].astype(int)
        y = c[1].astype(int)
        trace = go.Bar(
            x=x, y=y,
            #opacity = 0.8,
            name=name,
            marker=go.Marker(color=col),
            text=y,
            textposition='auto',
            )
        return trace

    def upd_bar2(self, entry_data, sql_stat, name, col):
        import pandas as pd
        import plotly.graph_objs as go
        import ch1
        a = ch1.IntoPostgres(entry_data[0], entry_data[1], entry_data[2], entry_data[3], entry_data[4])
        a.pcur(a.dbase, a.host, a.port, a.usern, a.pw)
        a.pX(sql_stat)
        b = a.cur.fetchall()
        c = pd.DataFrame(b)
        x = c[0].astype(int)
        y = c[1].astype(int)
        trace = go.Bar(
            x=x, y=y,
            opacity = 0.7,
            name=name,
            marker=go.Marker(color=col),
            text=y,
            textposition='auto',
            )
        return trace


    def upd_bar_n(self, entry_data, sql_stat, name, col):
        import pandas as pd
        import plotly.graph_objs as go
        import ch1
        a = ch1.IntoPostgres(entry_data[0], entry_data[1], entry_data[2], entry_data[3], entry_data[4])
        a.pcur(a.dbase, a.host, a.port, a.usern, a.pw)
        a.pX(sql_stat)
        b = a.cur.fetchall()
        c = pd.DataFrame(b)
        x = c[0]
        y = c[1].astype(int)
        trace = go.Bar(
            x=y, y=x,
            orientation = 'h',
            name=name,
            marker=go.Marker(color=col),
            text=y,
            textposition='auto',
            )
        return trace

    def upd_bar_n2(self, entry_data, sql_stat, name, col):
        import pandas as pd
        import plotly.graph_objs as go
        import ch1
        a = ch1.IntoPostgres(entry_data[0], entry_data[1], entry_data[2], entry_data[3], entry_data[4])
        a.pcur(a.dbase, a.host, a.port, a.usern, a.pw)
        a.pX(sql_stat)
        b = a.cur.fetchall()
        c = pd.DataFrame(b)
        x = c[0]
        y = c[1].astype(int)
        trace = go.Bar(
            x=y, y=x,
            opacity = 0.6,
            orientation = 'h',
            name=name,
            marker=go.Marker(color=col),
            #text=y,
            #textposition='auto',
            )
        return trace


    def upd_bar_t(self, entry_data, sql_stat, name, col):
        import pandas as pd
        import plotly.graph_objs as go
        import ch1
        a = ch1.IntoPostgres(entry_data[0], entry_data[1], entry_data[2], entry_data[3], entry_data[4])
        a.pcur(a.dbase, a.host, a.port, a.usern, a.pw)
        a.pX(sql_stat)
        b = a.cur.fetchall()
        c = pd.DataFrame(b)
        x = c[0]
        y = c[1].astype(int)
        trace = go.Bar(
            x=x, y=y,
            #orientation = 'h',
            name=name,
            marker=go.Marker(color=col),
            text=y,
            textposition='auto',
            )
        return trace

    def upd_bar_t2(self, entry_data, sql_stat, name, col):
        import pandas as pd
        import plotly.graph_objs as go
        import ch1
        a = ch1.IntoPostgres(entry_data[0], entry_data[1], entry_data[2], entry_data[3], entry_data[4])
        a.pcur(a.dbase, a.host, a.port, a.usern, a.pw)
        a.pX(sql_stat)
        b = a.cur.fetchall()
        c = pd.DataFrame(b)
        x = c[0]
        y = c[1].astype(int)
        trace = go.Bar(
            x=x, y=y,
            opacity = 0.6,
            #orientation = 'h',
            name=name,
            marker=go.Marker(color=col),
            text=y,
            textposition='auto',
            )
        return trace


    def upd_gr_kum(self, entry_data, sql_stat, name, col):
        import pandas as pd
        import plotly.graph_objs as go
        import ch1
        traces_kum = []
        
        def cummul(df):
            df = df[1]
            start = df[0]
            rest = df[1:]
            list_cum_end = []
            list_cum_end.append(start)
            for i in rest:
                list_cum_end.append(list_cum_end[-1] + i)
            return list_cum_end
            
        a = ch1.IntoPostgres(entry_data[0], entry_data[1], entry_data[2], entry_data[3], entry_data[4])
        a.pcur(a.dbase, a.host, a.port, a.usern, a.pw)
        a.pX(sql_stat)
        b = a.cur.fetchall()
        c = pd.DataFrame(b)
        x = c[0].astype(int)
        y_c = pd.DataFrame(cummul(c))
        y = y_c[0].astype(int)
        trace = go.Scatter(
            x=x, y=y,
            name=name,
            marker=go.Marker(color=col))
        return trace
     
    def upd_bar_kum(self, entry_data, sql_stat, name, col):
        import pandas as pd
        import plotly.graph_objs as go
        import ch1
        traces_kum = []
        
        def cummul(df):
            df = df[1]
            start = df[0]
            rest = df[1:]
            list_cum_end = []
            list_cum_end.append(start)
            for i in rest:
                list_cum_end.append(list_cum_end[-1] + i)
            return list_cum_end
            
        a = ch1.IntoPostgres(entry_data[0], entry_data[1], entry_data[2], entry_data[3], entry_data[4])
        a.pcur(a.dbase, a.host, a.port, a.usern, a.pw)
        a.pX(sql_stat)
        b = a.cur.fetchall()
        c = pd.DataFrame(b)
        x = c[0].astype(int)
        y_c = pd.DataFrame(cummul(c))
        y = y_c[0].astype(int)
        trace = go.Bar(
            x=x, y=y,
            name=name,
            marker=go.Marker(color=col),
            text=y,
            textposition='auto',)
        return trace

    def upd_scatter_t(self, entry_data, sql_stat, name, col):
        import pandas as pd
        import plotly.graph_objs as go
        import ch1
        import decimal as D
        traces_kum = []
            
        a = ch1.IntoPostgres(entry_data[0], entry_data[1], entry_data[2], entry_data[3], entry_data[4])
        a.pcur(a.dbase, a.host, a.port, a.usern, a.pw)
        a.pX(sql_stat)
        b = a.cur.fetchall()
        c = pd.DataFrame(b)
        x = c[0]
        y_c = pd.DataFrame(c[1]).astype(float)
        y_str = pd.DataFrame(y_c[1]).astype(str) + '%'
        size_y = pd.DataFrame(c[1]).astype(int)
        y = y_str[1]
        trace = go.Scatter(
            x=x, y=y,
            name=name,
            marker=go.Marker(color=col
                             ,size=size_y[1]**2
                             ,sizemode='area'
                             ,opacity=(size_y[1]+50)/100),
            mode = 'markers'

            #,
            #text=y,
            #textposition='auto',
            )
        return trace

    def layout1(self, traces, title, barmode, col_bg, col_txt):
        import plotly.graph_objs as go
        return {'data': traces,
                    'layout': go.Layout(
                        title=title,
                        showlegend=True,
                        barmode=barmode
                        ,plot_bgcolor=col_bg
                        ,paper_bgcolor=col_bg
                        ,font={'color': col_txt}
                        ,legend=go.Legend(
                            x=1.0,
                            y=1.0
                            ),
                      
                    
                        margin=go.Margin(l=50, r=50, t=60, b=40)
                        )}

    def layout2(self, traces, title, barmode, col_bg, col_txt):
        import plotly.graph_objs as go
        return {'data': traces,
                    'layout': go.Layout(
                        title=title,
                        showlegend=True,
                        barmode=barmode
                        ,plot_bgcolor=col_bg
                        ,paper_bgcolor=col_bg
                        ,font={'color': col_txt}
                        ,legend=go.Legend(
                            x=1.0,
                            y=1.0
                            ),
                    
                        margin=go.Margin(l=50, r=50, t=60, b=60)
                        )}

    def layout_kum(self, traces, title, col_bg, col_txt):
        import plotly.graph_objs as go
        return {'data': traces,
                    'layout': go.Layout(
                        title=title,
                        showlegend=True
                        ,plot_bgcolor=col_bg
                        ,paper_bgcolor=col_bg
                        ,font={'color': col_txt}
                        ,legend=go.Legend(
                            x=1.0,
                            y=1.0
                            ),
                    
                        margin=go.Margin(l=50, r=50, t=60, b=40)
                        )}

    def layout_n(self, traces, title, barmode, col_bg, col_txt):
        import plotly.graph_objs as go
        return {'data': traces,
                    'layout': go.Layout(
                        title=title,
                        showlegend=True,
                        barmode=barmode
                        ,plot_bgcolor=col_bg
                        ,paper_bgcolor=col_bg
                        ,font={'color': col_txt}
                        ,legend=go.Legend(
                            x=1.0,
                            y=1.0
                            ),
                    
                        margin=go.Margin(l=120, r=50, t=60, b=60)
                        )}


    def layout_t(self, traces, title, barmode, col_bg, col_txt):
        import plotly.graph_objs as go
        return {'data': traces,
                    'layout': go.Layout(
                        title=title,
                        showlegend=True,
                        barmode=barmode
                        ,plot_bgcolor=col_bg
                        ,paper_bgcolor=col_bg
                        ,font={'color': col_txt}
                        ,legend=go.Legend(
                            x=1.0,
                            y=1.0
                            ),
                    
                        margin=go.Margin(l=120, r=50, t=60, b=100)
                        )}

    def layout_custom_1(self, traces, title, col_bg, col_txt, l, r, t, b):
        import plotly.graph_objs as go
        return {'data': traces,
                    'layout': go.Layout(
                        title=title,
                        showlegend=True
                        #,barmode=barmode
                        ,plot_bgcolor=col_bg
                        ,paper_bgcolor=col_bg
                        ,font={'color': col_txt}
                        ,legend=go.Legend(
                            x=1.0,
                            y=1.0
                            ),
                    
                        margin=go.Margin(l=l, r=r, t=t, b=b)
                        )}