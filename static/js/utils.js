const COLORS = [
  '#4f6ef7','#22c55e','#f59e0b','#ef4444',
  '#8b5cf6','#06b6d4','#f97316','#ec4899',
  '#14b8a6','#6366f1','#84cc16','#e879f9'
];
function colorFor(name) {
  let h = 0;
  for (const c of name) h = (h * 31 + c.charCodeAt(0)) & 0xffffffff;
  return COLORS[Math.abs(h) % COLORS.length];
}


function initials(name) {
  return name.split(' ').slice(0,2).map(w => w[0]).join('').toUpperCase();
}


function today() { return new Date().toISOString().split('T')[0]; }


function fmtDate(str) {
  if (!str) return '—';
  const d = new Date(str);
  return d.toLocaleDateString('en-US', { month:'short', day:'numeric', year:'numeric' });
}


function stars(rating) {
  const full = Math.floor(rating);
  const half = rating % 1 >= 0.5 ? 1 : 0;
  const empty = 5 - full - half;
  return (
    '<span class="stars">' +
    '<i class="bi bi-star-fill"></i>'.repeat(full) +
    (half ? '<i class="bi bi-star-half"></i>' : '') +
    '<i class="bi bi-star"></i>'.repeat(empty) +
    '</span>' +
    ` <span class="rating-text">${rating.toFixed(1)}</span>`
  );
}


function pill(text, cls) {
  return `<span class="pill ${cls}">${text}</span>`;
}


function actionBtns(id, type) {
  return `
    <div class="action-btns">
      <button class="act-btn" title="View" onclick="openModal('${type}','${id}')"><i class="bi bi-eye"></i></button>
      <button class="act-btn" title="Edit"><i class="bi bi-pencil"></i></button>
      <button class="act-btn danger" title="Delete"><i class="bi bi-trash"></i></button>
    </div>`;
}


function avatarCell(name, sub) {
  const col = colorFor(name);
  return `
    <div class="user-cell">
      <div class="cell-ava" style="background:${col}">${initials(name)}</div>
      <div>
        <div class="cell-name">${name}</div>
        ${sub ? `<div class="cell-email">${sub}</div>` : ''}
      </div>
    </div>`;
}

function buildFooter(containerId, total, page, perPage) {
  const pages = Math.ceil(total / perPage);
  const start = (page - 1) * perPage + 1;
  const end   = Math.min(page * perPage, total);
  let btns = '';
  for (let i = 1; i <= pages; i++) {
    btns += `<button class="tf-btn${i === page ? ' active' : ''}" onclick="goPage('${containerId}',${i})">${i}</button>`;
  }
  return `
    <span>Showing ${start}–${end} of ${total} records</span>
    <div class="tf-pages">
      <button class="tf-btn" onclick="goPage('${containerId}',${Math.max(1,page-1)})"><i class="bi bi-chevron-left"></i></button>
      ${btns}
      <button class="tf-btn" onclick="goPage('${containerId}',${Math.min(pages,page+1)})"><i class="bi bi-chevron-right"></i></button>
    </div>`;
}


const DATA = {

  students: [
    { id:'S001', name:'Sok Dara',      email:'sokdara@school.edu',     class:'10A', parent:'Sok Vibol',    phone:'012-111-222', attendance:92, gpa:3.7, status:'active',   joined:'2023-09-01' },
    { id:'S002', name:'Chan Bopha',    email:'chanbopha@school.edu',   class:'10A', parent:'Chan Ratha',   phone:'012-222-333', attendance:78, gpa:3.1, status:'active',   joined:'2023-09-01' },
    { id:'S003', name:'Hout Sreyleak', email:'houtsreyleak@school.edu',class:'11B', parent:'Hout Mony',    phone:'012-333-444', attendance:97, gpa:4.0, status:'active',   joined:'2022-09-01' },
    { id:'S004', name:'Noun Piseth',   email:'nounpiseth@school.edu',  class:'9C',  parent:'Noun Kanha',   phone:'012-444-555', attendance:81, gpa:2.9, status:'active',   joined:'2024-01-10' },
    { id:'S005', name:'Mao Dina',      email:'maodina@school.edu',     class:'12A', parent:'Mao Vireak',   phone:'012-555-666', attendance:100,gpa:4.0, status:'active',   joined:'2021-09-01' },
    { id:'S006', name:'Prak Sophea',   email:'praksophea@school.edu',  class:'8B',  parent:'Prak Bunna',   phone:'012-666-777', attendance:85, gpa:3.3, status:'active',   joined:'2024-09-01' },
    { id:'S007', name:'Lim Chanthy',   email:'limchanthy@school.edu',  class:'10B', parent:'Lim Sitha',    phone:'012-777-888', attendance:88, gpa:3.5, status:'active',   joined:'2023-09-01' },
    { id:'S008', name:'Keo Daravy',    email:'keodary@school.edu',     class:'11A', parent:'Keo Puthea',   phone:'012-888-999', attendance:74, gpa:2.7, status:'inactive', joined:'2022-09-01' },
    { id:'S009', name:'Sam Ratha',     email:'samratha@school.edu',    class:'9A',  parent:'Sam Sokha',    phone:'012-990-001', attendance:95, gpa:3.9, status:'active',   joined:'2024-01-15' },
    { id:'S010', name:'Ros Sreyneth',  email:'rossrey@school.edu',     class:'12B', parent:'Ros Phal',     phone:'012-001-111', attendance:91, gpa:3.6, status:'active',   joined:'2021-09-01' },
    { id:'S011', name:'Chhun Leakna',  email:'chhunl@school.edu',      class:'8A',  parent:'Chhun Bora',   phone:'012-112-223', attendance:83, gpa:3.0, status:'active',   joined:'2024-09-01' },
    { id:'S012', name:'Ouk Pisey',     email:'oukpisey@school.edu',    class:'7B',  parent:'Ouk Dara',     phone:'012-223-334', attendance:96, gpa:3.8, status:'active',   joined:'2025-01-10' },
  ],


  teachers: [
    { id:'T01', name:'Meas Sopheak',    email:'msopheak@school.edu',   subject:'Mathematics', classes:'10A, 11B',    rating:4.5, joined:'2019-08-15', status:'active' },
    { id:'T02', name:'Chhun Leakna',    email:'cleakna@school.edu',    subject:'Science',     classes:'9A, 10B',     rating:4.2, joined:'2020-09-01', status:'active' },
    { id:'T03', name:'Ros Sotheavy',    email:'rsotheavy@school.edu',  subject:'English',     classes:'8A, 9C',      rating:4.7, joined:'2018-06-01', status:'active' },
    { id:'T04', name:'Nhem Bunthoeun',  email:'nbunthoeun@school.edu', subject:'History',     classes:'11A, 12B',    rating:3.9, joined:'2021-01-10', status:'leave'  },
    { id:'T05', name:'Ouk Pisey',       email:'opisey@school.edu',     subject:'Khmer',       classes:'7A, 7B, 8C',  rating:4.6, joined:'2017-09-01', status:'active' },
    { id:'T06', name:'Heng Sokha',      email:'hsokha@school.edu',     subject:'Geography',   classes:'9B, 10C',     rating:4.1, joined:'2022-08-20', status:'active' },
    { id:'T07', name:'Pich Sreymom',    email:'psreymom@school.edu',   subject:'Chemistry',   classes:'11C, 12A',    rating:4.3, joined:'2020-02-15', status:'active' },
    { id:'T08', name:'Mao Visal',       email:'mvisal@school.edu',     subject:'Physics',     classes:'10A, 12C',    rating:4.0, joined:'2021-09-01', status:'active' },
  ],


  parents: [
    { id:'P01', name:'Sok Vibol',    email:'sokvibol@gmail.com',   student:'Sok Dara',       class:'10A', phone:'012-111-222', lastActive:'Today' },
    { id:'P02', name:'Chan Ratha',   email:'chanratha@gmail.com',  student:'Chan Bopha',     class:'10A', phone:'012-222-333', lastActive:'Yesterday' },
    { id:'P03', name:'Hout Mony',    email:'houtmony@gmail.com',   student:'Hout Sreyleak',  class:'11B', phone:'012-333-444', lastActive:'2 days ago' },
    { id:'P04', name:'Noun Kanha',   email:'nounkanha@gmail.com',  student:'Noun Piseth',    class:'9C',  phone:'012-444-555', lastActive:'Today' },
    { id:'P05', name:'Mao Vireak',   email:'maovireak@gmail.com',  student:'Mao Dina',       class:'12A', phone:'012-555-666', lastActive:'3 days ago' },
    { id:'P06', name:'Prak Bunna',   email:'prakbunna@gmail.com',  student:'Prak Sophea',    class:'8B',  phone:'012-666-777', lastActive:'Today' },
    { id:'P07', name:'Lim Sitha',    email:'limsitha@gmail.com',   student:'Lim Chanthy',    class:'10B', phone:'012-777-888', lastActive:'1 week ago' },
    { id:'P08', name:'Keo Puthea',   email:'keoputhea@gmail.com',  student:'Keo Daravy',     class:'11A', phone:'012-888-999', lastActive:'Yesterday' },
  ],


  staff: [
    { id:'ST01', name:'Kem Sokha',     email:'ksokha@school.edu',     role:'Secretary',    dept:'Administration', phone:'012-321-001', status:'active' },
    { id:'ST02', name:'Lay Sreymom',   email:'lsreymom@school.edu',   role:'Accountant',   dept:'Finance',        phone:'012-321-002', status:'active' },
    { id:'ST03', name:'Rith Visal',    email:'rvisal@school.edu',     role:'IT Support',   dept:'Technology',     phone:'012-321-003', status:'active' },
    { id:'ST04', name:'Pen Ratana',    email:'pratana@school.edu',    role:'Librarian',    dept:'Library',        phone:'012-321-004', status:'leave'  },
    { id:'ST05', name:'Nhem Channary', email:'nchannary@school.edu',  role:'Nurse',        dept:'Health',         phone:'012-321-005', status:'active' },
    { id:'ST06', name:'Sok Piseth',    email:'sopiseth@school.edu',   role:'Security',     dept:'Security',       phone:'012-321-006', status:'active' },
    { id:'ST07', name:'Meas Dara',     email:'mdara@school.edu',      role:'Janitor',      dept:'Maintenance',    phone:'012-321-007', status:'active' },
  ],


  classes: [
    { id:'C01', name:'7A',  teacher:'Ouk Pisey',      subject:'Khmer',       students:32, capacity:35, attendance:91, color:'#4f6ef7' },
    { id:'C02', name:'8A',  teacher:'Ros Sotheavy',   subject:'English',     students:30, capacity:35, attendance:88, color:'#22c55e' },
    { id:'C03', name:'8B',  teacher:'Meas Sopheak',   subject:'Mathematics', students:34, capacity:35, attendance:85, color:'#f59e0b' },
    { id:'C04', name:'9A',  teacher:'Chhun Leakna',   subject:'Science',     students:31, capacity:35, attendance:93, color:'#ef4444' },
    { id:'C05', name:'9C',  teacher:'Nhem Bunthoeun', subject:'History',     students:28, capacity:35, attendance:79, color:'#8b5cf6' },
    { id:'C06', name:'10A', teacher:'Meas Sopheak',   subject:'Mathematics', students:33, capacity:35, attendance:94, color:'#06b6d4' },
    { id:'C07', name:'10B', teacher:'Heng Sokha',     subject:'Geography',   students:29, capacity:35, attendance:90, color:'#f97316' },
    { id:'C08', name:'11B', teacher:'Pich Sreymom',   subject:'Chemistry',   students:27, capacity:35, attendance:87, color:'#ec4899' },
    { id:'C09', name:'12A', teacher:'Mao Visal',      subject:'Physics',     students:25, capacity:35, attendance:95, color:'#14b8a6' },
  ],


  attendance: [
    { student:'Sok Dara',      class:'10A', timeIn:'07:42', status:'present', notified:false, remark:'' },
    { student:'Chan Bopha',    class:'10A', timeIn:'—',     status:'absent',  notified:true,  remark:'Sick' },
    { student:'Hout Sreyleak', class:'11B', timeIn:'07:38', status:'present', notified:false, remark:'' },
    { student:'Noun Piseth',   class:'9C',  timeIn:'08:05', status:'present', notified:false, remark:'Late' },
    { student:'Mao Dina',      class:'12A', timeIn:'07:30', status:'present', notified:false, remark:'' },
    { student:'Prak Sophea',   class:'8B',  timeIn:'—',     status:'absent',  notified:true,  remark:'No reason' },
    { student:'Lim Chanthy',   class:'10B', timeIn:'07:50', status:'present', notified:false, remark:'' },
    { student:'Keo Daravy',    class:'11A', timeIn:'—',     status:'leave',   notified:true,  remark:'Approved leave' },
    { student:'Sam Ratha',     class:'9A',  timeIn:'07:45', status:'present', notified:false, remark:'' },
    { student:'Ros Sreyneth',  class:'12B', timeIn:'07:55', status:'present', notified:false, remark:'' },
  ],


  exams: [
    { name:'Mid-Term 2025', subject:'Mathematics', class:'10A, 11B', date:'2025-03-10', teacher:'Meas Sopheak',   status:'upcoming' },
    { name:'Mid-Term 2025', subject:'Science',     class:'9A, 10B',  date:'2025-03-11', teacher:'Chhun Leakna',  status:'upcoming' },
    { name:'Mid-Term 2025', subject:'English',     class:'8A, 9C',   date:'2025-03-12', teacher:'Ros Sotheavy',  status:'upcoming' },
    { name:'Unit Test 4',   subject:'Khmer',       class:'7A, 7B',   date:'2025-02-14', teacher:'Ouk Pisey',     status:'approved' },
    { name:'Unit Test 4',   subject:'Chemistry',   class:'11C, 12A', date:'2025-02-20', teacher:'Pich Sreymom',  status:'approved' },
  ],


  leaves: [
    { id:'L001', applicant:'Sok Dara',      type:'Student', from:'2025-02-22', to:'2025-02-23', days:2, reason:'Medical',     parent:'Approved', status:'review'   },
    { id:'L002', applicant:'Chan Bopha',    type:'Student', from:'2025-02-24', to:'2025-02-24', days:1, reason:'Family',      parent:'Pending',  status:'pending'  },
    { id:'L003', applicant:'Hout Sreyleak', type:'Student', from:'2025-02-19', to:'2025-02-19', days:1, reason:'Appointment', parent:'Approved', status:'approved' },
    { id:'L004', applicant:'Nhem Bunthoeun',type:'Teacher', from:'2025-02-10', to:'2025-02-20', days:10,reason:'Personal',   parent:'N/A',      status:'approved' },
    { id:'L005', applicant:'Pen Ratana',    type:'Staff',   from:'2025-03-01', to:'2025-03-05', days:5, reason:'Medical',     parent:'N/A',      status:'pending'  },
    { id:'L006', applicant:'Keo Daravy',    type:'Student', from:'2025-02-21', to:'2025-02-21', days:1, reason:'Sick',        parent:'Approved', status:'approved' },
    { id:'L007', applicant:'Noun Piseth',   type:'Student', from:'2025-03-10', to:'2025-03-10', days:1, reason:'Exam prep',   parent:'Pending',  status:'pending'  },
    { id:'L008', applicant:'Mao Dina',      type:'Student', from:'2025-04-01', to:'2025-04-02', days:2, reason:'Travel',      parent:'Approved', status:'review'   },
  ],


  fees: [
    { student:'Sok Dara',      class:'10A', type:'Tuition',   amount:150, paid:150, due:'2025-03-01', status:'paid'    },
    { student:'Chan Bopha',    class:'10A', type:'Tuition',   amount:150, paid:0,   due:'2025-02-28', status:'overdue' },
    { student:'Hout Sreyleak', class:'11B', type:'Tuition',   amount:150, paid:150, due:'2025-03-01', status:'paid'    },
    { student:'Noun Piseth',   class:'9C',  type:'Tuition',   amount:150, paid:75,  due:'2025-03-01', status:'partial' },
    { student:'Mao Dina',      class:'12A', type:'Tuition',   amount:150, paid:150, due:'2025-03-01', status:'paid'    },
    { student:'Prak Sophea',   class:'8B',  type:'Tuition',   amount:150, paid:0,   due:'2025-03-01', status:'unpaid'  },
    { student:'Lim Chanthy',   class:'10B', type:'Lab Fee',   amount:30,  paid:30,  due:'2025-02-15', status:'paid'    },
    { student:'Keo Daravy',    class:'11A', type:'Lab Fee',   amount:30,  paid:0,   due:'2025-02-15', status:'overdue' },
    { student:'Sam Ratha',     class:'9A',  type:'Activity',  amount:25,  paid:25,  due:'2025-03-10', status:'paid'    },
    { student:'Ros Sreyneth',  class:'12B', type:'Graduation',amount:80,  paid:80,  due:'2025-04-01', status:'paid'    },
  ],


  notices: [
    { title:'Mid-Term Examination Schedule', date:'Feb 20, 2025', body:'Mid-term examinations will be held from March 10–14, 2025. Students are advised to review their timetables and prepare accordingly.', tags:['Academic','Exams'],      color:'#4f6ef7' },
    { title:'Parent-Teacher Meeting',        date:'Feb 18, 2025', body:'A parent-teacher meeting is scheduled for March 15, 2025 at 9:00 AM. All parents are encouraged to attend to discuss their child\'s academic progress.', tags:['Meeting','Parents'],    color:'#22c55e' },
    { title:'Annual Sports Day',             date:'Feb 15, 2025', body:'The Annual Sports Day will be held on April 5, 2025. Students interested in participating should register with their class teachers by March 25.', tags:['Event','Sports'],       color:'#f59e0b' },
    { title:'Library New Arrivals',          date:'Feb 12, 2025', body:'The school library has received new books across Science, Literature, and History. Students are encouraged to visit and borrow during library hours.', tags:['Library'],             color:'#8b5cf6' },
    { title:'School Closure – Khmer New Year',date:'Feb 10, 2025',body:'The school will be closed from April 14–16, 2025 for the Khmer New Year holiday. Regular classes resume on April 17.', tags:['Holiday'],              color:'#ef4444' },
    { title:'Science Fair Registration',     date:'Feb 8, 2025',  body:'Students interested in the inter-school Science Fair scheduled for May 2025 should register their project proposals by March 30, 2025.', tags:['Academic','Science'],  color:'#06b6d4' },
  ],


  events: [
    { title:'Mid-Term Exams',      date:'Mar 10',  color:'#4f6ef7', type:'Academic' },
    { title:'Parent-Teacher Meet', date:'Mar 15',  color:'#22c55e', type:'Meeting' },
    { title:'Science Fair',        date:'May 2',   color:'#8b5cf6', type:'Event' },
    { title:'Sports Day',          date:'Apr 5',   color:'#f59e0b', type:'Event' },
    { title:'Khmer New Year',      date:'Apr 14',  color:'#ef4444', type:'Holiday' },
  ],


  attendanceWeek: [
    { day:'Mon', present:88, absent:12 },
    { day:'Tue', present:91, absent:9  },
    { day:'Wed', present:79, absent:21 },
    { day:'Thu', present:94, absent:6  },
    { day:'Fri', present:85, absent:15 },
    { day:'Sat', present:72, absent:28 },
    { day:'Sun', present:68, absent:32 },
  ],


  grades: [
    { grade:'A',  count:124, color:'#22c55e' },
    { grade:'B',  count:310, color:'#4f6ef7' },
    { grade:'C',  count:280, color:'#f59e0b' },
    { grade:'D',  count:145, color:'#f97316' },
    { grade:'F',  count:62,  color:'#ef4444' },
  ],


  topPerformers: [
    { rank:1, name:'Mao Dina',      class:'12A', score:98.5, color:'#f59e0b' },
    { rank:2, name:'Hout Sreyleak', class:'11B', score:97.2, color:'#94a3b8' },
    { rank:3, name:'Sam Ratha',     class:'9A',  score:95.8, color:'#f97316' },
    { rank:4, name:'Ouk Pisey',     class:'7B',  score:94.1, color:'#4f6ef7' },
    { rank:5, name:'Ros Sreyneth',  class:'12B', score:93.7, color:'#8b5cf6' },
  ],


  recentLeaves: [
    { student:'Sok Dara',       date:'Feb 22', status:'review'   },
    { student:'Chan Bopha',     date:'Feb 24', status:'pending'  },
    { student:'Hout Sreyleak',  date:'Feb 19', status:'approved' },
    { student:'Keo Daravy',     date:'Feb 21', status:'approved' },
    { student:'Noun Piseth',    date:'Mar 10', status:'pending'  },
  ],


  notifications: [
    { title:'Attendance Alerts',     desc:'Notify parents when student is absent',      key:'n1', on:true  },
    { title:'Leave Updates',         desc:'Send email when leave status changes',        key:'n2', on:true  },
    { title:'Fee Reminders',         desc:'Remind parents of upcoming fee due dates',    key:'n3', on:false },
    { title:'Exam Results',          desc:'Alert students when results are published',   key:'n4', on:true  },
    { title:'Event Announcements',   desc:'Notify all users of upcoming school events',  key:'n5', on:true  },
    { title:'System Maintenance',    desc:'Admin alerts for system downtime',            key:'n6', on:false },
  ],
};


function filterTable(input, tableId) {
  const q = input.value.toLowerCase();
  const rows = document.querySelectorAll(`#${tableId} tbody tr`);
  rows.forEach(row => {
    row.style.display = row.textContent.toLowerCase().includes(q) ? '' : 'none';
  });
}


const PAGE_STATE = {};

function goPage(tableId, page) {
  PAGE_STATE[tableId] = page;
  if (tableId === 'studentFooter') renderStudents();
  else if (tableId === 'teacherFooter') renderTeachers();
  else if (tableId === 'parentFooter') renderParents();
  else if (tableId === 'staffFooter') renderStaff();
}