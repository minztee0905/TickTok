#!/usr/bin/env python3
"""Build BPMN 2.0 models, BPMNDI and SVG previews from a shared process model.

No third-party package is needed. These are descriptive, non-executable models.
Run from the repository root: python3 scripts/generate_diagrams.py
"""
from pathlib import Path
from html import escape
import math
import textwrap
import xml.etree.ElementTree as E

DOCS = Path(__file__).resolve().parents[1] / 'docs' / 'ba'

def artifact_path(filename):
    """Keep each editable model and preview beside its documentation."""
    name = Path(filename)
    if name.stem == 'use-cases':
        destination = DOCS / 'use-cases' / ('diagram' + name.suffix)
    else:
        process = name.stem.removeprefix('bpmn-')
        destination = DOCS / 'bpmn' / process / ('diagram' + name.suffix)
    destination.parent.mkdir(parents=True, exist_ok=True)
    return destination
NS = {'bpmn': 'http://www.omg.org/spec/BPMN/20100524/MODEL',
      'bpmndi': 'http://www.omg.org/spec/BPMN/20100524/DI',
      'dc': 'http://www.omg.org/spec/DD/20100524/DC',
      'di': 'http://www.omg.org/spec/DD/20100524/DI',
      'xsi': 'http://www.w3.org/2001/XMLSchema-instance'}
for prefix, uri in NS.items():
    E.register_namespace(prefix, uri)

def el(parent, tag, **attrs):
    prefix, local = tag.split(':')
    return E.SubElement(parent, '{'+NS[prefix]+'}'+local, {k: str(v) for k, v in attrs.items()})

def svg_text(x, y, value, width=31, size=15, anchor='middle', color='#172033'):
    lines = [line for part in value.split('\n') for line in (textwrap.wrap(part, width=width) or [''])]
    start = y - (len(lines)-1)*size*0.62
    # Separate text elements also work in macOS NSImage, whose SVG importer
    # ignores some tspan positioning attributes.
    return '<g>'+''.join('<text x="%s" y="%s" text-anchor="%s" fill="%s" font-size="%s">%s</text>' % (
        x, start+i*size*1.24, anchor, color, size, escape(line)) for i,line in enumerate(lines))+'</g>'

class Graph:
    def __init__(self, key, title, lanes, height):
        self.key, self.title, self.lanes, self.height = key, title, lanes, height
        self.nodes, self.flows = {}, []
        self.lane_width = 350
        self.width = 70 + len(lanes)*self.lane_width

    def n(self, key, kind, label, lane, y):
        x = 70 + self.lane_width*lane + self.lane_width/2
        w, h = (44,44) if kind.endswith('Event') else (64,64) if 'Gateway' in kind else (278,68)
        self.nodes[key] = dict(kind=kind, name=label, lane=lane, x=x-w/2, y=y-h/2, w=w, h=h)
        return key

    def f(self, source, target, label='', condition='', route=None, default=False):
        self.flows.append(dict(id='Flow_'+str(len(self.flows)+1), source=source, target=target,
                               name=label, condition=condition, route=route, default=default))

    def points(self, f):
        a,b = self.nodes[f['source']], self.nodes[f['target']]
        ax,ay=a['x']+a['w']/2,a['y']+a['h']/2
        bx,by=b['x']+b['w']/2,b['y']+b['h']/2
        if f['route'] is not None:
            route=f['route']
            # Route includes exact boundary anchors, not just intermediate bends.
            return route
        if abs(ax-bx)<1:
            return [(ax,ay+(a['h']/2 if by>ay else -a['h']/2)),(bx,by+(-b['h']/2 if by>ay else b['h']/2))]
        if abs(ay-by)<1:
            return [(ax+(a['w']/2 if bx>ax else -a['w']/2),ay),(bx+(-b['w']/2 if bx>ax else b['w']/2),by)]
        return [(ax+(a['w']/2 if bx>ax else -a['w']/2),ay),(bx,ay),(bx,by+(-b['h']/2 if by>ay else b['h']/2))]

    def label_position(self, f):
        pts = self.points(f)
        a,b = max(zip(pts,pts[1:]), key=lambda pair: abs(pair[1][0]-pair[0][0])+abs(pair[1][1]-pair[0][1]))
        x,y=(a[0]+b[0])/2,(a[1]+b[1])/2
        if abs(a[0]-b[0])<1 and b[1]>a[1] and 'Gateway' in self.nodes[f['source']]['kind']:
            y=min(b[1]-8,max(y,a[1]+65))
        if abs(a[0]-b[0])<1:
            return (x-12,y,'end') if x>self.width-150 else (x+12,y,'start')
        return (x,y-11,'middle')

    def write(self):
        key=self.key
        root=E.Element('{'+NS['bpmn']+'}definitions', id='Definitions_'+key,
                       targetNamespace='https://ticktok.local/analysis/'+key,
                       exporter='TickTok BA diagrams', exporterVersion='1.0')
        collaboration=el(root,'bpmn:collaboration',id='Collaboration_'+key)
        participant=el(collaboration,'bpmn:participant',id='Participant_'+key,name=self.title,processRef='Process_'+key)
        process=el(root,'bpmn:process',id='Process_'+key,name=self.title,isExecutable='false')
        el(process,'bpmn:documentation').text='Quy trình nghiệp vụ TickTok. Mô hình phân tích, không thực thi; thao tác SDK và callback được biểu diễn bằng service task.'
        laneset=el(process,'bpmn:laneSet',id='LaneSet_'+key)
        for i,label in enumerate(self.lanes):
            lane=el(laneset,'bpmn:lane',id='Lane_'+key+'_'+str(i),name=label)
            for k,n in self.nodes.items():
                if n['lane']==i: el(lane,'bpmn:flowNodeRef').text=k
        for k,n in self.nodes.items():
            incoming=[f for f in self.flows if f['target']==k]
            outgoing=[f for f in self.flows if f['source']==k]
            attrs=dict(id=k,name=n['name'])
            default=next((f for f in outgoing if f['default']),None)
            if default: attrs['default']=default['id']
            if 'Gateway' in n['kind']:
                attrs['gatewayDirection']='Diverging' if len(outgoing)>1 else 'Converging'
            node=el(process,'bpmn:'+n['kind'],**attrs)
            for f in incoming: el(node,'bpmn:incoming').text=f['id']
            for f in outgoing: el(node,'bpmn:outgoing').text=f['id']
        for f in self.flows:
            flow=el(process,'bpmn:sequenceFlow',id=f['id'],sourceRef=f['source'],targetRef=f['target'],name=f['name'])
            if f['condition']:
                cond=el(flow,'bpmn:conditionExpression')
                cond.set('{'+NS['xsi']+'}type','bpmn:tFormalExpression')
                cond.text=f['condition']
        diagram=el(root,'bpmndi:BPMNDiagram',id='Diagram_'+key)
        plane=el(diagram,'bpmndi:BPMNPlane',id='Plane_'+key,bpmnElement='Collaboration_'+key)
        shape=el(plane,'bpmndi:BPMNShape',id='DI_Participant_'+key,bpmnElement='Participant_'+key,isHorizontal='false')
        el(shape,'dc:Bounds',x=30,y=70,width=self.width-30,height=self.height-100)
        for i,label in enumerate(self.lanes):
            shape=el(plane,'bpmndi:BPMNShape',id='DI_Lane_'+key+'_'+str(i),bpmnElement='Lane_'+key+'_'+str(i),isHorizontal='false')
            el(shape,'dc:Bounds',x=70+i*self.lane_width,y=70,width=self.lane_width,height=self.height-100)
        for k,n in self.nodes.items():
            shape=el(plane,'bpmndi:BPMNShape',id='DI_'+k,bpmnElement=k)
            if 'Gateway' in n['kind']: shape.set('isMarkerVisible','true')
            el(shape,'dc:Bounds',x=n['x'],y=n['y'],width=n['w'],height=n['h'])
            if n['kind'].endswith('Event') or 'Gateway' in n['kind']:
                label=el(shape,'bpmndi:BPMNLabel')
                el(label,'dc:Bounds',x=n['x']-75,y=n['y']+n['h']+5,width=n['w']+150,height=45)
        for f in self.flows:
            edge=el(plane,'bpmndi:BPMNEdge',id='DI_'+f['id'],bpmnElement=f['id'])
            pts=self.points(f)
            for x,y in pts: el(edge,'di:waypoint',x=x,y=y)
            if f['name']:
                x,y,anchor=self.label_position(f)
                label=el(edge,'bpmndi:BPMNLabel')
                labelx=x if anchor=='start' else x-130 if anchor=='end' else x-65
                el(label,'dc:Bounds',x=labelx,y=y-14,width=130,height=30)
        E.indent(root,space='  ')
        E.ElementTree(root).write(artifact_path(key+'.bpmn'),encoding='utf-8',xml_declaration=True)
        self.svg()
        self.validate()

    def svg(self):
        s=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.width}" height="{self.height}" viewBox="0 0 {self.width} {self.height}">',
           '<title>'+escape(self.title)+'</title>',
           '<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#475569"/></marker></defs>',
           f'<rect x="0" y="0" width="{self.width}" height="{self.height}" fill="#ffffff"/>',
           '<g font-family="Arial, Helvetica, sans-serif">',svg_text(self.width/2,30,self.title,width=100,size=21)]
        for i,l in enumerate(self.lanes):
            x=70+i*self.lane_width
            s.append(f'<rect x="{x}" y="70" width="350" height="{self.height-100}" fill="{["#f8fafc","#f1f5f9","#f8fafc","#f1f5f9"][i]}" stroke="#94a3b8"/>')
            s.append(f'<rect x="{x}" y="70" width="350" height="45" fill="#dbeafe" stroke="#94a3b8"/>')
            s.append(svg_text(x+175,98,l,width=35,size=16))
        for f in self.flows:
            pts=self.points(f)
            s.append('<polyline points="'+' '.join(f'{x},{y}' for x,y in pts)+'" fill="none" stroke="#475569" stroke-width="1.5" marker-end="url(#arrow)"/>')
            a,b=pts[-2],pts[-1]
            angle=math.atan2(b[1]-a[1],b[0]-a[0])
            corners=[b,(b[0]-9*math.cos(angle)+4*math.sin(angle),b[1]-9*math.sin(angle)-4*math.cos(angle)),(b[0]-9*math.cos(angle)-4*math.sin(angle),b[1]-9*math.sin(angle)+4*math.cos(angle))]
            s.append('<polygon points="'+' '.join(f'{x},{y}' for x,y in corners)+'" fill="#475569"/>')
            if f['default']:
                x,y=pts[0]; s.append(f'<path d="M{x-5} {y+7} l10 -10" stroke="#475569"/>')
            if f['name']:
                x,y,anchor=self.label_position(f)
                s.append(svg_text(x,y,f['name'],width=22,size=12,anchor=anchor,color='#334155'))
        for k,n in self.nodes.items():
            x,y,w,h=n['x'],n['y'],n['w'],n['h']; cx,cy=x+w/2,y+h/2
            kind=n['kind']
            if kind.endswith('Event'):
                s.append(f'<circle cx="{cx}" cy="{cy}" r="22" fill="white" stroke="#172033" stroke-width="{3.7 if kind=="endEvent" else 1.7}"/>')
                s.append(svg_text(cx,cy+43,n['name'],width=25,size=13))
            elif 'Gateway' in kind:
                s.append(f'<polygon points="{cx},{y} {x+w},{cy} {cx},{y+h} {x},{cy}" fill="white" stroke="#172033" stroke-width="1.6"/>')
                s.append(svg_text(cx,cy+7,'+' if kind=='parallelGateway' else '×',size=34))
                s.append(svg_text(cx,cy+53,n['name'],width=26,size=13))
            else:
                s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="9" fill="white" stroke="#172033" stroke-width="1.4"/>')
                if kind=='userTask':
                    s.append(f'<circle cx="{x+16}" cy="{y+13}" r="4" fill="none" stroke="#334155"/><path d="M{x+9} {y+27} q0 -10 7 -10 q7 0 7 10 M{x+16} {y+18} v10" fill="none" stroke="#334155"/>')
                if kind=='serviceTask':
                    s.append(svg_text(x+16,y+22,'⚙',size=20))
                s.append(svg_text(cx,cy+4,n['name'],width=32,size=14))
        s.append('</g></svg>')
        (artifact_path(self.key+'.svg')).write_text('\n'.join(s))

    def validate(self):
        nodeids=set(self.nodes)
        assert len(nodeids)==len(self.nodes)
        for f in self.flows:
            assert f['source'] in nodeids and f['target'] in nodeids
            if f['condition']: assert self.nodes[f['source']]['kind']=='exclusiveGateway'
        start=[k for k,n in self.nodes.items() if n['kind']=='startEvent']
        ends={k for k,n in self.nodes.items() if n['kind']=='endEvent'}
        seen=set(start)
        while True:
            new=seen|{f['target'] for f in self.flows if f['source'] in seen}
            if new==seen: break
            seen=new
        assert seen==nodeids,('Unreachable',nodeids-seen)
        for k,n in self.nodes.items():
            if k not in ends: assert any(f['source']==k for f in self.flows),('No outgoing',k)
            if k not in start: assert any(f['target']==k for f in self.flows),('No incoming',k)
        root=E.parse(artifact_path(self.key+'.bpmn')).getroot()
        ids=[x.attrib['id'] for x in root.iter() if 'id' in x.attrib]
        assert len(ids)==len(set(ids))
        for x in root.iter():
            for a in ['sourceRef','targetRef','bpmnElement','processRef','default']:
                if a in x.attrib: assert x.attrib[a] in ids
        E.parse(artifact_path(self.key+'.svg'))
        print(f'{self.key}: {len(nodeids)} nodes, {len(self.flows)} flows; XML, DI, refs, reachability OK')

def task_process():
    g=Graph('bpmn-01-create-task','BPMN-01 · Tạo công việc và đặt lời nhắc',['Tương tác người dùng / UI','Ứng dụng TickTok','Firestore SDK / callback','Android: quyền và alarm'],1780)
    N=g.n; F=g.f
    N('T_start','startEvent','Bấm thêm công việc',0,160)
    N('T_input','userTask','Nhập nội dung, ngày, ưu tiên và lời nhắc; bấm Gửi',0,270)
    N('T_empty','exclusiveGateway','Nội dung sau trim rỗng?',1,270)
    N('T_hint','task','Hiện gợi ý nhập nội dung; giữ form',0,420)
    N('T_prepare','task','Tách dòng đầu thành tiêu đề; ngày mặc định hôm nay',1,460)
    N('T_badreminder','exclusiveGateway','Lời nhắc quá khứ / sau ngày hạn?',1,600)
    N('T_clear','task','Xóa reminderTime về 0; báo lý do; vẫn tạo task',0,600)
    N('T_merge','exclusiveGateway','Tiếp tục xử lý',1,740)
    N('T_auth','exclusiveGateway','Có UID?',1,860)
    N('T_noauth','task','Yêu cầu đăng nhập; không ghi task',0,860)
    N('T_authend','endEvent','Dừng; form chưa lưu',0,990)
    N('T_add','serviceTask','Gọi add(task) vào users/UID/tasks; chờ kết quả',2,860)
    N('T_result','exclusiveGateway','Callback thành công?',2,1010)
    N('T_error','task','Báo lỗi ghi; giữ form để người dùng xử lý',1,1010)
    N('T_errorend','endEvent','Chưa xác nhận lưu',1,1150)
    N('T_id','task','Nhận document ID; gửi update createdAt không chờ',2,1170)
    N('T_future','exclusiveGateway','reminderTime > hiện tại?',3,1170)
    N('T_cancel','serviceTask','Hủy alarm cũ nếu có',2,1320)
    N('T_request','serviceTask','Nếu Android 13+ chưa cấp: yêu cầu quyền thông báo; không chờ',3,1320)
    N('T_schedule','serviceTask','Thay alarm: exact nếu được phép; nếu không, dùng inexact',3,1460)
    N('T_success','task','Thông báo thêm thành công; đóng bottom sheet',1,1580)
    N('T_end','endEvent','Task đã được ghi',1,1690)
    F('T_start','T_input');F('T_input','T_empty');F('T_empty','T_hint','Rỗng','trim(rawInput) == ""',route=[(563,270),(435,270),(435,420),(384,420)]);F('T_hint','T_input')
    F('T_empty','T_prepare','Có nội dung',default=True);F('T_prepare','T_badreminder')
    F('T_badreminder','T_clear','Không hợp lệ','reminder > 0 and (reminder <= now or reminder >= dueDate + 86400000)')
    F('T_clear','T_merge',route=[(384,600),(410,600),(410,740),(563,740)]);F('T_badreminder','T_merge','Hợp lệ / không đặt',default=True);F('T_merge','T_auth')
    F('T_auth','T_noauth','Không',default=True);F('T_noauth','T_authend');F('T_auth','T_add','Có','uid != null');F('T_add','T_result')
    F('T_result','T_error','Lỗi',default=True);F('T_error','T_errorend');F('T_result','T_id','Thành công','callback.success')
    F('T_id','T_future');F('T_future','T_cancel','Không',default=True,route=[(1327,1170),(1440,1170),(1440,1240),(1100,1240),(1100,1320),(1084,1320)]);F('T_future','T_request','Có','reminder > now')
    F('T_request','T_schedule');F('T_cancel','T_success');F('T_schedule','T_success');F('T_success','T_end')
    g.write()

def pomo_process():
    g=Graph('bpmn-02-focus-completion','BPMN-02 · Kết thúc phiên FOCUS và ghi lịch sử',['Điều khiển phiên','Chuẩn bị lịch sử / callback','Firestore SDK'],2000)
    N=g.n;F=g.f
    N('P_start','startEvent','FOCUS hết giờ hoặc bấm Complete',0,165)
    N('P_auto','exclusiveGateway','Tự hết giờ?',0,290)
    N('P_fork','parallelGateway','Hai nhánh không chờ nhau',0,755)
    N('P_break','task','Đổi sang BREAK 5 phút và tự khởi chạy',0,900)
    N('P_cycleend','endEvent','Chu kỳ tiếp tục',0,1045)
    N('P_autoprep','task','duration = totalMillis; resetAfterSave = false',1,450)
    N('P_autouid','exclusiveGateway','Có UID?',1,600)
    N('P_autoskip','task','Bỏ qua ghi lịch sử',1,755)
    N('P_autowrite','serviceTask','Gửi add lịch sử: totalMillis, tên task, thời điểm lưu; chưa chờ',2,600)
    N('P_autowait','serviceTask','Đợi callback ghi lịch sử',2,755)
    N('P_autoresult','exclusiveGateway','Callback thành công?',2,900)
    N('P_autook','task','Toast đã lưu nếu có Context',2,1045)
    N('P_autofail','task','Toast lỗi nếu có Context; không dừng chu kỳ',1,1045)
    N('P_saveend','endEvent','Kết thúc nhánh lưu',2,1190)
    N('P_manualstop','task','Complete: hủy timer, đặt isRunning/isPaused = false',0,1190)
    N('P_manualprep','task','duration = totalMillis; resetAfterSave = true',1,1190)
    N('P_manualuid','exclusiveGateway','Có UID?',1,1345)
    N('P_manualauth','task','Báo cần đăng nhập nếu có Context',0,1345)
    N('P_manualwrite','serviceTask','Gọi add lịch sử; chờ callback thành công hoặc thất bại',2,1345)
    N('P_manualresult','exclusiveGateway','Callback thành công?',2,1495)
    N('P_manualok','task','Toast đã lưu nếu có Context',2,1640)
    N('P_manualfail','task','Toast lỗi nếu có Context',1,1640)
    N('P_reset','task','Reset về FOCUS đã chọn; không tự chạy',0,1780)
    N('P_end','endEvent','Sẵn sàng phiên mới',0,1900)
    F('P_start','P_auto');F('P_auto','P_autoprep','Hết giờ','trigger == timerFinish');F('P_fork','P_break');F('P_break','P_cycleend');F('P_fork','P_autowait',route=[(277,755),(330,755),(330,820),(945,820),(945,789)])
    F('P_autoprep','P_autouid');F('P_autouid','P_autoskip','Không',default=True);F('P_autouid','P_autowrite','Có','uid != null')
    F('P_autoskip','P_break',route=[(456,755),(410,755),(410,900),(384,900)]);F('P_autowrite','P_fork',route=[(806,600),(760,600),(760,680),(245,680),(245,723)]);F('P_autowait','P_autoresult');F('P_autoresult','P_autook','Thành công','callback.success');F('P_autoresult','P_autofail','Lỗi',default=True)
    F('P_autook','P_saveend');F('P_autofail','P_saveend',route=[(734,1045),(760,1045),(760,1190),(923,1190)])
    # Explicit long route avoids crossing the automatic-cycle boxes.
    F('P_auto','P_manualstop','Complete',default=True,route=[(213,290),(95,290),(95,1190),(106,1190)])
    F('P_manualstop','P_manualprep');F('P_manualprep','P_manualuid');F('P_manualuid','P_manualauth','Không',default=True)
    F('P_manualauth','P_reset');F('P_manualuid','P_manualwrite','Có','uid != null');F('P_manualwrite','P_manualresult')
    F('P_manualresult','P_manualok','Thành công','callback.success');F('P_manualresult','P_manualfail','Lỗi',default=True)
    F('P_manualok','P_reset',route=[(945,1674),(945,1715),(245,1715),(245,1746)]);F('P_manualfail','P_reset');F('P_reset','P_end')
    g.write()

def event_process():
    g=Graph('bpmn-03-event-reminders','BPMN-03 · Lưu sự kiện và lập hai mốc nhắc',['Tương tác người dùng / UI','Ứng dụng TickTok','Firestore SDK / callback','Android: quyền và alarm'],2220)
    N=g.n;F=g.f
    N('E_start','startEvent','Thêm hoặc sửa sự kiện',0,160)
    N('E_input','userTask','Nhập tên, biểu tượng, chọn ngày; bấm Lưu',0,275)
    N('E_valid','exclusiveGateway','Có ngày và tên sau trim?',1,275)
    N('E_hint','task','Chưa ngày: Lưu tắt; thiếu tên: nhắc nhập',0,430)
    N('E_auth','exclusiveGateway','Có UID / ID sửa hợp lệ?',1,475)
    N('E_authfail','task','Báo lỗi; bật lại trạng thái Lưu',0,595)
    N('E_badend','endEvent','Chưa lưu sự kiện',0,730)
    N('E_save','serviceTask','Thêm mới hoặc update title/icon/targetDate; chờ callback',2,475)
    N('E_result','exclusiveGateway','Callback thành công?',2,630)
    N('E_error','task','Báo lỗi nếu Fragment còn gắn; cho sửa lại',1,630)
    N('E_errorend','endEvent','Chưa xác nhận lưu',1,780)
    N('E_timestamp','task','Nhận ID; chỉ khi thêm: gửi update createdAt không chờ',2,800)
    N('E_attached','exclusiveGateway','Fragment còn gắn?',2,950)
    N('E_detached','endEvent','Đã ghi; callback dừng',1,950)
    N('E_request','serviceTask','Yêu cầu quyền thông báo nếu cần; không chờ trả lời',3,950)
    N('E_manager','exclusiveGateway','AlarmManager khả dụng?',3,1110)
    N('E_cancel','serviceTask','Hủy cả hai alarm cũ của event',3,1270)
    N('E_times','task','Lần lượt lấy 08:00 ngày trước và 08:00 ngày diễn ra',3,1400)
    N('E_future','exclusiveGateway','Mốc đang xét > hiện tại?',3,1540)
    N('E_skip','task','Bỏ qua mốc đã qua',2,1540)
    N('E_schedule','serviceTask','Đặt alarm cho mốc này: exact nếu cho phép; nếu không inexact',3,1690)
    N('E_more','exclusiveGateway','Còn mốc chưa xét?',2,1830)
    N('E_success','task','Thông báo lưu thành công; đóng bottom sheet',1,1990)
    N('E_end','endEvent','Đã lưu; có thể có 0–2 alarm',1,2140)
    F('E_start','E_input');F('E_input','E_valid');F('E_valid','E_hint','Chưa hợp lệ',default=True,route=[(563,275),(435,275),(435,430),(384,430)]);F('E_hint','E_input')
    F('E_valid','E_auth','Hợp lệ','targetDate > 0 and trim(title) != ""')
    F('E_auth','E_authfail','Không',default=True);F('E_authfail','E_badend');F('E_auth','E_save','Có','uid != null and (not edit or validId)')
    F('E_save','E_result');F('E_result','E_error','Lỗi',default=True);F('E_error','E_errorend');F('E_result','E_timestamp','Thành công','callback.success')
    F('E_timestamp','E_attached');F('E_attached','E_detached','Không',default=True);F('E_attached','E_request','Có','fragment.isAdded')
    F('E_request','E_manager');F('E_manager','E_cancel','Có','alarmManager != null')
    F('E_manager','E_success','Không',default=True,route=[(1327,1110),(1445,1110),(1445,1990),(734,1990)])
    F('E_cancel','E_times');F('E_times','E_future');F('E_future','E_skip','Không',default=True);F('E_future','E_schedule','Có','triggerAt > now')
    F('E_skip','E_more');F('E_schedule','E_more')
    F('E_more','E_times','Có','hasNextSlot',route=[(977,1830),(1105,1830),(1105,1400),(1156,1400)])
    F('E_more','E_success','Không',default=True);F('E_success','E_end')
    g.write()

def usecases():
    cases=[('01','Đăng ký tài khoản'),('02','Đăng nhập tài khoản'),('03','Đăng nhập Google'),('04','Quản lý danh mục'),('05','Thêm công việc'),('06','Sửa công việc'),('07','Đổi trạng thái hoàn thành'),('08','Xóa công việc'),('09','Xem / lọc công việc'),('10','Tìm kiếm công việc'),('11','Quản lý sự kiện'),('12','Sử dụng Pomodoro'),('13','Xem thống kê tập trung'),('14','Chia sẻ thống kê'),('15','Cài đặt giao diện / âm thanh'),('16','Đổi mật khẩu'),('17','Đăng xuất'),('18','Nhập công việc bằng giọng nói')]
    auth=['01','02','03','16','17'];data=['04','05','06','07','08','09','10','11','12','13'];android=['05','06','07','08','11','12','14','18']
    p=['@startuml','left to right direction','skinparam shadowing false','skinparam packageStyle rectangle','skinparam defaultFontName Arial','actor "Người dùng" as User','actor "Firebase Authentication" as Auth','actor "Cloud Firestore" as DB','actor "Dịch vụ Android / ứng dụng nhận chia sẻ" as OS','rectangle "Ứng dụng TickTok" {']
    p += [f'  usecase "UC-{id}\\n{name}" as UC{id}' for id,name in cases]
    p += ['}']+[f'User -- UC{id}' for id,_ in cases]
    p += [f'UC{id} -- Auth' for id in auth]+[f'UC{id} -- DB' for id in data]+[f'UC{id} -- OS' for id in android]
    nl=chr(92)+'n'
    p += ['UC18 ..> UC05 : <<extend>>'+nl+'[nhập bằng giọng nói]',
          'UC18 ..> UC06 : <<extend>>'+nl+'[nhập bằng giọng nói]',
          'UC14 ..> UC13 : <<extend>>'+nl+'[chọn chia sẻ]',
          'note bottom of UC15','Âm thanh: hiện chỉ lưu lựa chọn;','chưa chi phối chuông Pomodoro.','end note',
          'note bottom of UC09','Lịch và ma trận nằm trong UC-09;','ma trận hiện phân nhóm theo priority.','end note','@enduml']
    (artifact_path('use-cases.puml')).write_text('\n'.join(p)+'\n')
    width,height=1560,1210
    s=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">','<title>TickTok — UML Use Case Diagram</title>','<defs><marker id="open" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto"><path d="M 0 0 L 10 5 L 0 10" fill="none" stroke="#0f766e"/></marker></defs>',f'<rect x="0" y="0" width="{width}" height="{height}" fill="#ffffff"/><g font-family="Arial, Helvetica, sans-serif">',svg_text(780,32,'TickTok — UML Use Case Diagram',width=70,size=24),'<rect x="220" y="65" width="1050" height="1090" fill="#f8fafc" stroke="#334155" stroke-width="2"/>',svg_text(745,96,'Ranh giới hệ thống: ứng dụng Android TickTok',width=65,size=17)]
    pos={id:(460 if i<9 else 1010,160+(i%9)*113) for i,(id,name) in enumerate(cases)}
    def actor(x,y,label):
        return f'<circle cx="{x}" cy="{y}" r="14" fill="white" stroke="#172033" stroke-width="2"/><path d="M{x} {y+14} v38 M{x-26} {y+29} h52 M{x} {y+52} l-24 30 M{x} {y+52} l24 30" fill="none" stroke="#172033" stroke-width="2"/>'+svg_text(x,y+108,label,width=21,size=15)
    # Primary actor associations terminate at the use case boundary; supporting links are gray.
    for id,_ in cases:
        x,y=pos[id]
        path=f'M115 585 L{x-185} {y}' if x==460 else f'M115 585 L205 585 L205 115 L745 115 L745 {y} L{x-185} {y}'
        s.append(f'<path d="{path}" stroke="#cbd5e1" fill="none"/>')
    for group,y in [(auth,160),(data,520),(android,900)]:
        for id in group:
            x,cy=pos[id]
            s.append(f'<path d="M{x+185} {cy} L1430 {y+40}" stroke="#d1d5db" fill="none"/>')
    for id,name in cases:
        x,y=pos[id]
        s.append(f'<ellipse cx="{x}" cy="{y}" rx="185" ry="36" fill="white" stroke="#334155" stroke-width="1.5"/>')
        s.append(svg_text(x,y-8,'UC-'+id+'\n'+name,width=36,size=15))
    # Extensions route in the wide center corridor, keeping labels away from node text.
    s.append('<path d="M825 1064 L745 1064 L745 612 L645 612" fill="none" stroke="#0f766e" stroke-dasharray="6 4" marker-end="url(#open)"/>')
    s.append('<path d="M655 607 L645 612 L655 617" fill="none" stroke="#0f766e"/>')
    s.append('<path d="M825 1064 L760 1064 L760 725 L645 725" fill="none" stroke="#0f766e" stroke-dasharray="6 4" marker-end="url(#open)"/>')
    s.append('<path d="M655 720 L645 725 L655 730" fill="none" stroke="#0f766e"/>')
    s.append(svg_text(738,1005,'«extend» UC-18 → UC-05/06',width=24,size=12,anchor='end',color='#0f766e'))
    s.append('<path d="M1010 576 L1010 535" fill="none" stroke="#0f766e" stroke-dasharray="6 4" marker-end="url(#open)"/>')
    s.append('<path d="M1005 545 L1010 535 L1015 545" fill="none" stroke="#0f766e"/>')
    s.append(svg_text(1090,560,'«extend»',width=20,size=12,color='#0f766e'))
    s += [actor(115,535,'Người dùng'),actor(1430,160,'Firebase Authentication'),actor(1430,520,'Cloud Firestore'),actor(1430,900,'Android / app nhận chia sẻ'),svg_text(780,1190,'Đường liền: association. Mũi tên đứt: extend. UC-18 mở rộng UC-05 và UC-06; UC-14 mở rộng UC-13.',width=130,size=13),'</g></svg>']
    (artifact_path('use-cases.svg')).write_text('\n'.join(s))
    E.parse(artifact_path('use-cases.svg'))
    print('use-cases: 18 use cases; PlantUML source and SVG preview created')

if __name__=='__main__':
    DOCS.mkdir(parents=True,exist_ok=True)
    task_process();pomo_process();event_process();usecases()
