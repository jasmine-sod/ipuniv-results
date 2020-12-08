<?php
header('Access-Control-Allow-Origin: *');
header("Access-Control-Allow-Headers: X-Requested-With");

$host="localhost";
$username="akshay_baweja";
$password="baweja9899";
$database="myipuresult";
$conn = mysqli_connect($host, $username, $password, $database);

// BASE URL : http://myipuresult.com/api/
$method = $_SERVER['REQUEST_METHOD'];
$data = explode('/', trim($_SERVER['PATH_INFO'], '/'));

$returnJSON = array();

if ($method == "GET") {
    switch ($data[0]) {
        case 'profile':
            if ($data[1] == "search") {
                $name = urldecode($data[2]);
                $sql = "SELECT name, enrolment_number, institute, course FROM students WHERE name LIKE '% ".$name ."' ";
                $sql  .= "OR name LIKE '".$name." %' OR name LIKE '% ".$name." %' OR name LIKE '".$name."'";
                $result = mysqli_query($conn, $sql);
                if (mysqli_num_rows($result)>0) {
                    $returnJSON['response'] = 'success';
                    $rows = array();
                    while ($row = mysqli_fetch_array($result)) {
                        $rowdata = array('enrolment_number' => $row['enrolment_number'],
                                        'name' => $row['name'],
                                        'institute' => $row['institute'],
                                        'course' => $row['course']);
                        array_push($rows, $rowdata);
                    }
                    $returnJSON['results'] = $rows;
                } else {
                    $returnJSON['response'] = 'error';
                    $returnJSON['error_description'] = 'Nobody Found';
                }
            } else {
                $enrolment_number = (string) $data[1];
                $sql = "SELECT name, enrolment_number, institute, course FROM students ";
                $sql .= "WHERE enrolment_number LIKE '".$enrolment_number. "'";
                $result = mysqli_query($conn, $sql);
                if (mysqli_num_rows($result)>0) {
                    $result = mysqli_fetch_array($result);
                    $returnJSON['response'] = 'success';
                    $returnJSON['enrolment_number'] = $result['enrolment_number'];
                    $returnJSON['name'] = $result['name'];
                    $returnJSON['institute'] = $result['institute'];
                    $returnJSON['course'] = $result['course'];
                } else {
                    $returnJSON['response'] = 'error';
                    $returnJSON['error_description'] = 'Enrolment Number not Found';
                }
            }
            break;
        case 'result':
            $enrolment_number = (string) $data[1];
            $ssql = "SELECT SID FROM students WHERE enrolment_number = $enrolment_number";
            $sid = mysqli_fetch_array(mysqli_query($conn, $ssql));
            $sid = $sid['SID'];

            if ($data[2] == null) {
                $sql = "SELECT students.enrolment_number, students.name, students.course, students.institute, ";
                $sql .= "subjects.paperID, subjects.code, subjects.name AS subject, marks.internal, marks.external, marks.total, ";
                $sql .= "marks.semester, marks.credits, marks.pass FROM ((marks ";
                $sql .= "INNER JOIN students ON marks.sid = students.sid) ";
                $sql .= "INNER JOIN subjects ON marks.paperID = subjects.paperID AND students.schemeID = subjects.schemeID) ";
                $sql .= "WHERE marks.sid = '".$sid."'";
                $result = mysqli_query($conn, $sql);
                if (mysqli_num_rows($result)>0) {
                    $returnJSON['response'] = 'success';
                    $rows = array();
                    $student = array();
                    $got_details = false;
                    while ($row = mysqli_fetch_array($result)) {
                        if ($got_details == false) {
                            $student['enrolment_number'] = $row['enrolment_number'];
                            $student['name'] = $row['name'];
                            $student['course'] = $row['course'];
                            $student['college'] = $row['institute'];
                            $returnJSON = array_merge($returnJSON, $student);
                            $got_details = true;
                        }
                        $rowdata = array('internal' => $row['internal'],
                                        'external' => $row['external'],
                                        'total' => $row['total'],
                                        'credits' => $row['credits'],
                                        'paper_id' => $row['paperID'],
                                        'code' => $row['code'],
                                        'name' => $row['subject'],
                                        'status' => $row['pass']);
                        if (!array_key_exists($row['semester'], $rows)) {
                            $rows[$row['semester']] = array();
                        }

                        array_push($rows[$row['semester']], $rowdata);
                    }
                    $returnJSON['results'] = $rows;
                } else {
                    $returnJSON['response'] = 'error';
                    $returnJSON['error_description'] = 'Enrolment Number not Found';
                    $returnJSON['student_id'] = $sid;
                }
            }
            elseif ($data[2] == 'latest') {
                $sql = "SELECT students.enrolment_number, students.name, students.course, students.institute, ";
                $sql .= "subjects.paperID, subjects.code, subjects.name AS subject, marks.internal, marks.external, marks.total, ";
                $sql .= "marks.semester, marks.credits, marks.pass FROM ((marks INNER JOIN students ON marks.sid = students.sid) ";
                $sql .= "INNER JOIN subjects ON marks.paperID = subjects.paperID AND students.schemeID = subjects.schemeID) ";
                $sql .= "WHERE marks.sid = '".$sid."' AND marks.semester = (SELECT MAX(marks.semester) FROM marks ";
                $sql .= "WHERE marks.sid = '".$sid."')";

                $result = mysqli_query($conn, $sql);
                if (mysqli_num_rows($result)>0) {
                    $returnJSON['response'] = 'success';
                    $rows = array();
                    $student = array();
                    $got_details = false;
                    while ($row = mysqli_fetch_array($result)) {
                        if ($got_details == false) {
                            $student['enrolment_number'] = $row['enrolment_number'];
                            $student['name'] = $row['name'];
                            $student['course'] = $row['course'];
                            $student['college'] = $row['institute'];
                            $student['semester'] = $row['semester'];
                            $returnJSON = array_merge($returnJSON, $student);
                            $got_details = true;
                        }
                        $rowdata = array('internal' => $row['internal'],
                                        'external' => $row['external'],
                                        'total' => $row['total'],
                                        'credits' => $row['credits'],
                                        'paper_id' => $row['paperID'],
                                        'code' => $row['code'],
                                        'name' => $row['subject'],
                                        'status' => $row['pass']);
                        
                        array_push($rows, $rowdata);
                    }
                    $returnJSON['results'] = $rows;
                } else {
                    $returnJSON['response'] = 'error';
                    $returnJSON['error_description'] = 'Enrolment Number not Found';
                }
            } else {
                $semester = $data[2];
                $sql = "SELECT students.enrolment_number, students.name, students.course, students.institute, ";
                $sql .= "subjects.paperID, subjects.code, subjects.name AS subject, marks.internal, marks.external, marks.total, ";
                $sql .= "marks.semester, marks.credits, marks.pass FROM ((marks INNER JOIN students ON marks.sid = students.sid) ";
                $sql .= "INNER JOIN subjects ON marks.paperID = subjects.paperID AND students.schemeID = subjects.schemeID) ";
                $sql .= "WHERE marks.sid = '".$sid."' AND marks.semester = '".$semester."'";
                $result = mysqli_query($conn, $sql);
                if (mysqli_num_rows($result)>0) {
                    $returnJSON['response'] = 'success';
                    $rows = array();
                    $student = array();
                    $got_details = false;
                    while ($row = mysqli_fetch_array($result)) {
                        if ($got_details == false) {
                            $student['enrolment_number'] = $row['enrolment_number'];
                            $student['name'] = $row['name'];
                            $student['course'] = $row['course'];
                            $student['college'] = $row['institute'];
                            $student['semester'] = $row['semester'];
                            $returnJSON = array_merge($returnJSON, $student);
                            $got_details = true;
                        }
                        $rowdata = array('internal' => $row['internal'],
                                        'external' => $row['external'],
                                        'total' => $row['total'],
                                        'credits' => $row['credits'],
                                        'paper_id' => $row['paperID'],
                                        'code' => $row['code'],
                                        'name' => $row['subject'],
                                        'status' => $row['pass']);
                        
                        array_push($rows, $rowdata);
                    }
                    $returnJSON['results'] = $rows;
                } else {
                    $returnJSON['response'] = 'error';
                    $returnJSON['error_description'] = 'Invalid Enrolment Number or Semester';
                }
            }
            break;
        default:
            $returnJSON['response'] = 'error';
                 $returnJSON['error_description'] = 'Invalid Directive';
    }
} else {
    $returnJSON['response'] = 'error';
    $returnJSON['error_description'] = 'Invalid Method';
}
if ($returnJSON['response'] == 'error') {
    http_response_code(400);
}
header("Content-Type: application/json");
echo json_encode($returnJSON);
